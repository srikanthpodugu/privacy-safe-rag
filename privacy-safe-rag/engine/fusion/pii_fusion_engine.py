from collections import defaultdict


class PIIFusionEngine:

    def __init__(self):

        self.weights = {

            "regex": 1.0,
            "presidio": 0.85,
            "llm": 0.7
        }

    # ==========================================================
    # MAIN MERGE FUNCTION
    # ==========================================================
    def merge(self, detections_list):

        fused = defaultdict(lambda: {

            "count": 0,
            "score": 0.0,
            "entities": []
        })

        # ======================================================
        # NORMALIZATION
        # ======================================================
        for item in detections_list:

            source = item["source"]

            results = item["results"]

            weight = self.weights.get(source, 0.5)

            for r in results:

                # ----------------------------------------------
                # PRESIDIO OBJECT
                # ----------------------------------------------
                if hasattr(r, "entity_type"):

                    entity_type = r.entity_type
                    start = r.start
                    end = r.end

                # ----------------------------------------------
                # DICT FORMAT
                # ----------------------------------------------
                else:

                    entity_type = r["entity_type"]
                    start = r["start"]
                    end = r["end"]

                key = (entity_type, start, end)

                fused[key]["count"] += 1
                fused[key]["score"] += weight
                fused[key]["entities"].append(r)

        # ======================================================
        # FINAL ENTITY SELECTION
        # ======================================================
        final_entities = []

        for (entity_type, start, end), data in fused.items():

            confidence = min(
                1.0,
                data["score"] / 1.5
            )

            if confidence < 0.5:
                continue

            final_entities.append({

                "entity_type": entity_type,

                "start": start,

                "end": end,

                "confidence": round(confidence, 3)
            })

        # ======================================================
        # SAFE REVERSE SORT
        # ======================================================
        final_entities = sorted(

            final_entities,

            key=lambda x: x["start"],

            reverse=True
        )

        return final_entities