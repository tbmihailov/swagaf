import json
import sys

import pandas as pd

if __name__ == "__main__":
    input_file = sys.argv[1]
    gold_status = sys.argv[2]

    cnli = pd.read_csv(input_file)

    output_file = input_file
    use_only_gold_examples = gold_status == "gold"
    if use_only_gold_examples:
        if input_file.endswith('train.csv'):
            cnli = cnli[cnli['gold-source'].str.startswith('gold')]
            output_file = output_file + ".gold"
        else:
            output_file = output_file + ".all"

    output_file = output_file + ".json"

    id_to_label = {0: "A", 1: "B", 2: "C", 3: "D"}

    row_id = 0
    with open(output_file, mode="w") as out_f:
        for _, row in cnli.iterrows():
            premise = row['sent1']
            endings = [row['ending{}'.format(i)] for i in range(4)]
            hypos = ['{} {}'.format(row['sent2'], end) for end in endings]

            json_item = {
                            "id": "{0}_{1:06d}".format(input_file, row_id),
                            "question": {"stem": premise,
                            "choices": [{"text": h_txt, "label": id_to_label[h_id]} for h_id, h_txt in enumerate(hypos)]
                                         },
                            "answerKey": id_to_label.get(row['label'], None) if hasattr(row, 'label') else None
                        }

            out_f.write(json.dumps(json_item))
            out_f.write("\n")
            row_id += 1

