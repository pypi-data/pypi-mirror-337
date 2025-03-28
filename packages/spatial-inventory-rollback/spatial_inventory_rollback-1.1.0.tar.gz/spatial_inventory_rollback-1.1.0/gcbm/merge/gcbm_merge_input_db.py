from __future__ import annotations
import os
import shutil
import sqlite3
import logging
import pandas as pd
from collections import defaultdict


null_classifier_value = "null (spatial rollback)"


class GrowthCurve:
    def __init__(self, name: str, classifiers: str):
        self.name = name
        self.classifiers = classifiers
        self.components = defaultdict(dict)

    def __eq__(self, other: "GrowthCurve") -> bool:
        # Name is excluded from equality checks since two different databases
        # could have a growth curve for the same classifier set under a
        # different name.
        return self.classifiers == other.classifiers

    def __hash__(self) -> int:
        # Name is excluded from the hash since two different databases could
        # have a growth curve for the same classifier set under a different
        # name.
        return 31 * 7 + sum(
            (hash(k) + hash(v) for k, v in self.classifiers.items())
        )


class TransitionRule:
    def __init__(
        self, name, transition_type, disturbance_type, age_after, regen_delay
    ):
        self.name = name
        self.transition_type = transition_type
        self.disturbance_type = disturbance_type
        self.age_after = age_after
        self.regen_delay = regen_delay
        self.classifiers_after = {}
        self.classifiers_match = {}

    def __eq__(self, other):
        # Name is excluded from equality checks since the same logical rule
        # could potentially be in two different databases under a different
        # name.
        return (
            self.transition_type == other.transition_type
            and self.disturbance_type == other.disturbance_type
            and self.age_after == other.age_after
            and self.regen_delay == other.regen_delay
            and self.classifiers_after == other.classifiers_after
            and self.classifiers_match == other.classifiers_match
        )

    def __hash__(self):
        # Name is excluded from the hash since the same logical rule could
        # potentially be in two different databases under a different name.
        return (
            31 * 17
            + hash(self.transition_type)
            + hash(self.disturbance_type)
            + hash(self.age_after)
            + hash(self.regen_delay)
            + sum(
                (hash(k) + hash(v) for k, v in self.classifiers_after.items())
            )
            + sum(
                (hash(k) + hash(v) for k, v in self.classifiers_match.items())
            )
        )


def get_merged_disturbance_types(gcbm_dbs):
    sql = """
          SELECT
              dt.name AS disturbance_type,
              dc.code AS category,
              lc.code AS land_class_transition
          FROM disturbance_type dt
          INNER JOIN disturbance_category dc
              ON dt.disturbance_category_id = dc.id
          LEFT JOIN land_class lc
              ON dt.transition_land_class_id = lc.id
          """

    disturbance_types = {}
    for db in gcbm_dbs:
        with sqlite3.connect(db) as conn:
            disturbance_types.update(
                {
                    disturbance_type: {
                        "category": category,
                        "land_class_transition": land_class_transition,
                    }
                    for (
                        disturbance_type,
                        category,
                        land_class_transition,
                    ) in conn.execute(sql)
                }
            )

    return disturbance_types


def load_disturbance_types(gcbm_db, disturbance_types):
    with sqlite3.connect(gcbm_db) as conn:
        row_count = conn.executemany(
            """
            INSERT OR IGNORE INTO disturbance_type (
                name, disturbance_category_id, transition_land_class_id)
            SELECT
                ? AS name,
                cat.id AS disturbance_category_id,
                lc.id AS transition_land_class_id
            FROM disturbance_category cat
            LEFT JOIN (SELECT id FROM land_class WHERE code = ?) AS lc
                ON 1 = 1
            WHERE cat.code = ?
            """,
            (
                (
                    disturbance_type,
                    parameters["land_class_transition"],
                    parameters["category"],
                )
                for disturbance_type, parameters in disturbance_types.items()
            ),
        ).rowcount

        logging.info(f"Loaded {row_count} new disturbance types.")


def get_merged_disturbance_matrices(gcbm_dbs):
    transfer_sql = """
        SELECT
            dm.name AS disturbance_matrix,
            source.name AS from_pool,
            sink.name AS to_pool,
            dmv.proportion
        FROM disturbance_matrix dm
        INNER JOIN disturbance_matrix_value dmv
            ON dm.id = dmv.disturbance_matrix_id
        INNER JOIN pool source
            ON dmv.source_pool_id = source.id
        INNER JOIN pool sink
            ON dmv.sink_pool_id = sink.id
        WHERE dm.name IN ({})
        """

    association_sql = """
        SELECT
            dm.name AS disturbance_matrix,
            dt.name AS disturbance_type,
            admin.name AS admin_boundary,
            eco.name AS eco_boundary
        FROM disturbance_matrix dm
        INNER JOIN disturbance_matrix_association dma
            ON dm.id = dma.disturbance_matrix_id
        INNER JOIN disturbance_type dt
            ON dma.disturbance_type_id = dt.id
        INNER JOIN spatial_unit spu
            ON dma.spatial_unit_id = spu.id
        INNER JOIN admin_boundary admin
            ON spu.admin_boundary_id = admin.id
        INNER JOIN eco_boundary eco
            ON spu.eco_boundary_id = eco.id
        WHERE dm.name IN ({})
        """

    matrices = defaultdict(
        lambda: {
            "transfers": [],  # (from, to, proportion)
            "associations": [],  # (disturbance type, admin, eco)
        }
    )

    all_matrices = set()

    for db in gcbm_dbs:
        with sqlite3.connect(db) as conn:
            db_matrices = set(
                (
                    row[0]
                    for row in conn.execute(
                        "SELECT DISTINCT name FROM disturbance_matrix"
                    )
                )
            )

            new_matrices = db_matrices - all_matrices
            if not new_matrices:
                continue

            all_matrices = all_matrices.union(new_matrices)
            placeholders = ",".join("?" * len(new_matrices))
            for matrix, from_pool, to_pool, proportion in conn.execute(
                transfer_sql.format(placeholders), list(new_matrices)
            ):
                matrices[matrix]["transfers"].append(
                    (from_pool, to_pool, proportion)
                )

            for matrix, dist_type, admin, eco in conn.execute(
                association_sql.format(placeholders), list(new_matrices)
            ):
                matrices[matrix]["associations"].append(
                    (dist_type, admin, eco)
                )

    return matrices


def load_disturbance_matrices(gcbm_db, matrices):
    with sqlite3.connect(gcbm_db) as conn:
        loaded = 0
        for matrix, parameters in matrices.items():
            result = conn.execute(
                "INSERT OR IGNORE INTO disturbance_matrix (name) VALUES (?)",
                [matrix],
            )
            matrix_exists = result.rowcount == 0
            if matrix_exists:
                continue

            dm_id = result.lastrowid
            loaded += 1

            conn.executemany(
                """
                INSERT INTO disturbance_matrix_value (
                    disturbance_matrix_id, source_pool_id, sink_pool_id,
                    proportion
                )
                SELECT
                    ? AS disturbance_matrix_id,
                    source.id AS source_pool_id,
                    sink.id AS sink_pool_id,
                    ? AS proportion
                FROM pool source, pool sink
                WHERE source.name = ?
                    AND sink.name = ?
                """,
                (
                    (dm_id, proportion, source, sink)
                    for source, sink, proportion in parameters["transfers"]
                ),
            )

            conn.executemany(
                """
                INSERT INTO disturbance_matrix_association (
                    spatial_unit_id, disturbance_type_id,
                    disturbance_matrix_id
                )
                SELECT
                    spu.id AS spatial_unit_id,
                    dt.id AS disturbance_type_id,
                    ? AS disturbance_matrix_id
                FROM disturbance_type dt, spatial_unit spu
                INNER JOIN admin_boundary admin
                    ON spu.admin_boundary_id = admin.id
                INNER JOIN eco_boundary eco
                    ON spu.eco_boundary_id = eco.id
                WHERE dt.name = ?
                    AND admin.name = ?
                    AND eco.name = ?
                """,
                (
                    (dm_id,) + association
                    for association in parameters["associations"]
                ),
            )

        logging.info(f"Loaded {loaded} new disturbance matrices.")


def get_merged_classifiers(gcbm_dbs):
    sql = """
          SELECT name, value
          FROM classifier c
          INNER JOIN classifier_value cv
              ON c.id = cv.classifier_id
          """

    classifiers = defaultdict(lambda: {null_classifier_value})
    for db in gcbm_dbs:
        with sqlite3.connect(db) as conn:
            for name, value in conn.execute(sql):
                classifiers[name].add(value)

    return classifiers


def load_new_classifiers(gcbm_db, classifiers):
    with sqlite3.connect(gcbm_db) as conn:
        row_count = conn.executemany(
            "INSERT OR IGNORE INTO classifier (name) VALUES (?)",
            ([key] for key in classifiers.keys()),
        ).rowcount

        logging.info(f"Loaded {row_count} new classifiers.")

        for classifier, classifier_values in classifiers.items():
            conn.executemany(
                """
                INSERT OR IGNORE INTO classifier_value (
                    classifier_id, value, description
                )
                SELECT c.id, ? AS value, ? AS description
                FROM classifier c
                WHERE c.name = ?
                """,
                ((value, value, classifier) for value in classifier_values),
            )


def get_soft_transition_rules(gcbm_db):
    # Gets all the "soft" (rule-based) transition rules from a database.
    with sqlite3.connect(gcbm_db) as conn:
        transition_rules = [
            TransitionRule(
                rule_name,
                transition_type,
                disturbance_type,
                age_after,
                regen_delay,
            )
            for (
                rule_name,
                transition_type,
                disturbance_type,
                age_after,
                regen_delay,
            ) in conn.execute(
                """
                SELECT
                    t.description AS rule_name, tt.name AS transition_type,
                    dt.name AS disturbance_type, t.age AS age_after,
                    t.regen_delay
                FROM transition_rule tr
                INNER JOIN transition t
                    ON tr.transition_id = t.id
                INNER JOIN transition_type tt
                    ON t.transition_type_id = tt.id
                INNER JOIN disturbance_type dt
                    ON tr.disturbance_type_id = dt.id
                """
            )
        ]

        for transition_rule in transition_rules:
            transition_rule.classifiers_after = dict(
                conn.execute(
                    """
                    SELECT name, value
                    FROM transition t
                    INNER JOIN transition_classifier_value tcv
                        ON t.id = tcv.transition_id
                    INNER JOIN classifier_value cv
                        ON tcv.classifier_value_id = cv.id
                    INNER JOIN classifier c
                        ON cv.classifier_id = c.id
                    WHERE t.description = ?
                    """,
                    (transition_rule.name,),
                )
            )

            transition_rule.classifiers_match = dict(
                conn.execute(
                    """
                    SELECT name, value
                    FROM transition t
                    INNER JOIN transition_rule tr
                        ON t.id = tr.transition_id
                    INNER JOIN transition_rule_classifier_value tcv
                        ON tr.id = tcv.transition_rule_id
                    INNER JOIN classifier_value cv
                        ON tcv.classifier_value_id = cv.id
                    INNER JOIN classifier c
                        ON cv.classifier_id = c.id
                    WHERE t.description = ?
                    """,
                    (transition_rule.name,),
                )
            )

        transition_rules = set(transition_rules)

        return transition_rules


def load_new_transition_rules(gcbm_db, transition_rules):
    existing_transition_rules = get_soft_transition_rules(gcbm_db)
    new_transition_rules = transition_rules - existing_transition_rules

    with sqlite3.connect(gcbm_db) as conn:
        for rule in new_transition_rules:
            new_rule_id = conn.execute(
                """
                INSERT INTO transition (
                    description, transition_type_id, age, regen_delay
                )
                SELECT
                    ? AS description,
                    tt.id AS transition_type_id,
                    ? AS age,
                    ? AS regen_delay
                FROM transition_type tt
                WHERE tt.name = ?
                """,
                (
                    rule.name,
                    rule.age_after,
                    rule.regen_delay,
                    rule.transition_type,
                ),
            ).lastrowid

            conn.executemany(
                """
                INSERT INTO transition_classifier_value (
                    transition_id, classifier_value_id
                )
                SELECT ? AS transition_id, cv.id AS classifier_value_id
                FROM classifier c
                INNER JOIN classifier_value cv
                    ON c.id = cv.classifier_id
                WHERE c.name = ?
                    AND cv.value = ?
                """,
                (
                    (new_rule_id,) + item
                    for item in rule.classifiers_after.items()
                ),
            )

            conn.execute(
                """
                INSERT INTO transition_rule (
                    transition_id, disturbance_type_id
                )
                SELECT ? AS transition_id, dt.id AS disturbance_type_id
                FROM disturbance_type dt
                WHERE dt.name = ?
                """,
                (new_rule_id, rule.disturbance_type),
            )

            conn.executemany(
                """
                INSERT INTO transition_rule_classifier_value (
                    transition_rule_id, classifier_value_id
                )
                SELECT
                    tr.id AS transition_rule_id,
                    cv.id AS classifier_value_id
                FROM transition_rule tr, classifier c
                INNER JOIN classifier_value cv
                    ON c.id = cv.classifier_id
                WHERE tr.transition_id = ?
                    AND c.name = ?
                    AND cv.value = ?
                """,
                (
                    (new_rule_id,) + item
                    for item in rule.classifiers_match.items()
                ),
            )

    logging.info(f"Loaded {len(new_transition_rules)} new transition rules.")


def delete_direct_attached_transition_rules(gcbm_db):
    with sqlite3.connect(gcbm_db) as conn:
        conn.execute(
            """
            DELETE FROM transition_classifier_value
            WHERE transition_id IN (
                SELECT t.id
                FROM transition t
                LEFT JOIN transition_rule tr
                    ON t.id = tr.transition_id
                WHERE tr.id IS NULL
            )
            """
        )

        conn.execute(
            """
            DELETE FROM transition
            WHERE id IN (
                SELECT t.id
                FROM transition t
                LEFT JOIN transition_rule tr
                    ON t.id = tr.transition_id
                WHERE tr.id IS NULL
            )
            """
        )


def refresh_transition_rules(gcbm_db):
    # Delete any direct-attached transition rules - these will be replaced
    # by a new, unified set of direct-attached transition rules in the usual
    # tiler-generated csv file for the merged disturbance layers.
    delete_direct_attached_transition_rules(gcbm_db)

    with sqlite3.connect(gcbm_db) as conn:
        # Make sure each transition rule has the full set of classifiers, with
        # missing ones getting a special null value. Need this for the matching
        # part of "soft" transition rules only; destination classifier values can
        # be a subset of the landscape classifier set.
        conn.execute(
            """
            INSERT INTO transition_rule_classifier_value (
                transition_rule_id, classifier_value_id
            )
            SELECT
                placeholders.transition_rule_id,
                placeholders.classifier_value_id
            FROM (
                SELECT
                    tcv.transition_rule_id,
                    cv.classifier_id,
                    cv.id AS classifier_value_id
                FROM transition_rule_classifier_value tcv, classifier_value cv
                WHERE cv.value = ?
                GROUP BY tcv.transition_rule_id, cv.classifier_id, cv.id
            ) AS placeholders
            LEFT JOIN (
                transition_rule_classifier_value tcv
                INNER JOIN classifier_value cv
                    ON tcv.classifier_value_id = cv.id
                INNER JOIN classifier c
                    ON cv.classifier_id = c.id
            ) ON placeholders.transition_rule_id = tcv.transition_rule_id
                AND placeholders.classifier_id = c.id
            WHERE tcv.classifier_value_id IS NULL
            """,
            (null_classifier_value,),
        )


def replace_direct_attached_transition_rules(gcbm_db, transition_rules_csv):
    delete_direct_attached_transition_rules(gcbm_db)

    with sqlite3.connect(gcbm_db) as conn:
        transitions = pd.read_csv(transition_rules_csv)
        max_new_id = transitions.id.max()
        for sql in (
            "UPDATE transition SET id = id + ?",
            "UPDATE transition_classifier_value SET transition_id = transition_id + ?",
            "UPDATE transition_rule SET transition_id = transition_id + ?",
        ):
            conn.execute(sql, (max_new_id,))

        for _, row in transitions.iterrows():
            conn.execute(
                """
                INSERT INTO transition (
                    id, description, transition_type_id, age, regen_delay
                )
                SELECT
                    ? AS id,
                    ? AS description,
                    tt.id AS transition_type_id,
                    ? AS age,
                    ? AS regen_delay
                FROM transition_type tt
                WHERE tt.name = ?
                """,
                (
                    row.id,
                    row.id,
                    row.age_after,
                    row.regen_delay,
                    "absolute",
                ),
            )

            conn.executemany(
                """
                INSERT INTO transition_classifier_value (
                    transition_id, classifier_value_id
                )
                SELECT ? AS transition_id, cv.id AS classifier_value_id
                FROM classifier c
                INNER JOIN classifier_value cv
                    ON c.id = cv.classifier_id
                WHERE c.name = ?
                    AND cv.value = ?
                """,
                (
                    (row.id,) + item
                    for item in row.items()
                    if item[0] not in ("id", "regen_delay", "age_after")
                ),
            )


def get_growth_curves(gcbm_db):
    growth_curves = set()
    with sqlite3.connect(gcbm_db) as conn:
        for gcid, name in conn.execute(
            "SELECT gc.id, gc.description AS name FROM growth_curve gc"
        ):
            classifiers = {
                classifier_name: classifier_value
                for classifier_name, classifier_value in conn.execute(
                    """
                    SELECT c.name, cv.value
                    FROM growth_curve_classifier_value gccv
                    INNER JOIN classifier_value cv
                        ON gccv.classifier_value_id = cv.id
                    INNER JOIN classifier c
                        ON cv.classifier_id = c.id
                    WHERE gccv.growth_curve_id = ?
                    """,
                    (gcid,),
                )
            }

            gc = GrowthCurve(name, classifiers)
            for species_name, age, volume in conn.execute(
                """
                SELECT
                    s.name AS species_name,
                    gccv.age,
                    gccv.merchantable_volume
                FROM growth_curve_component gcc
                INNER JOIN growth_curve_component_value gccv
                    ON gcc.id = gccv.growth_curve_component_id
                INNER JOIN species s
                    ON gcc.species_id = s.id
                WHERE gcc.growth_curve_id = ?
                """,
                (gcid,),
            ):
                gc.components[species_name][age] = volume

            growth_curves.add(gc)

    return growth_curves


def load_new_growth_curves(gcbm_db, growth_curves):
    existing_growth_curves = get_growth_curves(gcbm_db)
    new_growth_curves = growth_curves - existing_growth_curves

    with sqlite3.connect(gcbm_db) as conn:
        for gc in new_growth_curves:
            new_gc_id = conn.execute(
                "INSERT INTO growth_curve (description) VALUES (?)", [gc.name]
            ).lastrowid

            conn.executemany(
                """
                INSERT INTO growth_curve_classifier_value (
                    growth_curve_id, classifier_value_id
                )
                SELECT ? AS growth_curve_id, cv.id AS classifier_value_id
                FROM classifier c
                INNER JOIN classifier_value cv
                    ON c.id = cv.classifier_id
                WHERE c.name = ?
                    AND cv.value = ?
                """,
                (
                    (new_gc_id, name, value)
                    for name, value in gc.classifiers.items()
                ),
            )

            for species, volumes in gc.components.items():
                component_id = conn.execute(
                    """
                    INSERT INTO growth_curve_component (
                        growth_curve_id, species_id
                    )
                    SELECT ? AS growth_curve_id, s.id AS species_id
                    FROM species s
                    WHERE s.name = ?
                    """,
                    (new_gc_id, species),
                ).lastrowid

                conn.executemany(
                    """
                    INSERT INTO growth_curve_component_value (
                        growth_curve_component_id, age, merchantable_volume
                    ) VALUES (?, ?, ?)
                    """,
                    (
                        (component_id, age, volume)
                        for age, volume in volumes.items()
                    ),
                )

    logging.info(f"Loaded {len(new_growth_curves)} new growth curves.")


def refresh_growth_curves(gcbm_db):
    # Make sure each growth curve has the full set of classifiers, with missing
    # ones getting a special null value.
    with sqlite3.connect(gcbm_db) as conn:
        conn.execute(
            """
            INSERT INTO growth_curve_classifier_value (
                growth_curve_id, classifier_value_id
            )
            SELECT
                placeholders.growth_curve_id,
                placeholders.classifier_value_id
            FROM (
                SELECT
                    gccv.growth_curve_id,
                    cv.classifier_id,
                    cv.id AS classifier_value_id
                FROM growth_curve_classifier_value gccv, classifier_value cv
                WHERE cv.value = ?
                GROUP BY gccv.growth_curve_id, cv.classifier_id, cv.id
            ) AS placeholders
            LEFT JOIN (
                growth_curve_classifier_value gccv
                INNER JOIN classifier_value cv
                    ON gccv.classifier_value_id = cv.id
                INNER JOIN classifier c
                    ON cv.classifier_id = c.id
            ) ON placeholders.growth_curve_id = gccv.growth_curve_id
                AND placeholders.classifier_id = c.id
            WHERE gccv.classifier_value_id IS NULL
            """,
            (null_classifier_value,),
        )


def check_mergeability(gcbm_dbs):
    # Merging species types is not currently supported.
    with sqlite3.connect(gcbm_dbs[0]) as conn:
        known_species = set(
            (row[0] for row in conn.execute("SELECT name FROM species"))
        )

    for gcbm_db in gcbm_dbs[1:]:
        with sqlite3.connect(gcbm_db) as conn:
            merge_species = set(
                (
                    row[0]
                    for row in conn.execute(
                        """
                        SELECT DISTINCT s.name AS species
                        FROM growth_curve_component gcc
                        INNER JOIN species s
                            ON gcc.species_id = s.id
                        """
                    )
                )
            )

            unknown_species = merge_species - known_species
            if unknown_species:
                raise RuntimeError("Can't merge different species types.")


def merge_input_dbs(input_dbs: list[str], output_db: str) -> None:
    unique_input_dbs = set((os.path.abspath(db) for db in input_dbs))
    if len(unique_input_dbs) == 1:
        logging.info("No input databases to merge.")
        return

    check_mergeability(input_dbs)

    logging.info(f"Merging GCBM input databases into {output_db}")

    if os.path.exists(output_db):
        os.remove(output_db)

    os.makedirs(os.path.dirname(output_db), exist_ok=True)
    shutil.copyfile(input_dbs[0], output_db)

    classifiers = get_merged_classifiers(input_dbs)
    load_new_classifiers(output_db, classifiers)

    dist_types = get_merged_disturbance_types(input_dbs)
    load_disturbance_types(output_db, dist_types)

    matrices = get_merged_disturbance_matrices(input_dbs)
    load_disturbance_matrices(output_db, matrices)

    for db in input_dbs[1:]:
        transition_rules = get_soft_transition_rules(db)
        load_new_transition_rules(output_db, transition_rules)

    refresh_transition_rules(output_db)

    for db in input_dbs[1:]:
        growth_curves = get_growth_curves(db)
        load_new_growth_curves(output_db, growth_curves)

    refresh_growth_curves(output_db)
