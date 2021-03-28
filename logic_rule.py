import pandas as pd
from mapping_question import questions
import itertools
from random import choice


def prepared_file_uploaded(file):
    df = pd.read_excel(file, engine="openpyxl")
    df.fillna("", inplace=True)
    df = df.astype(str).apply(lambda x: x.str.lower())
    df_as_nested_list = df.to_numpy().tolist()
    return df_as_nested_list


def data_generating(df_as_nested_list, n_try=5):
    combinations = []
    for index, row in enumerate(df_as_nested_list):
        # generate number_generation times on each row
        """
        row display like this:
        ['dưới 18 tuổi',
         'nam ',
         'thpt trở xuống',
         'dưới 1 triệu',
         'ít hơn 1 giờ',
         'rd 1,2',
         'rd 2,3',
         'rd 4,5',
         '',
         '',
         '',
         ...
         """
        new_row = row[:4] + [value for value in row[4:] if value != ""]
        if len(new_row) < 13:
            new_row = new_row + [""] * (13 - len(new_row))

        # remove trailing space
        new_row = [value.strip() for value in new_row]

        print(new_row)
        if "th" not in new_row[0]:
            try:
                if new_row[0] != "":
                    starting_with_number = questions.get(new_row[0])
                else:
                    starting_with_number = combinations[-1][0]
            except Exception as e:
                print(f"excaption starting_with_number: {e}")

            # generate number_generation times ford each row
            number_generation = 0
            while number_generation < n_try:
                gen_data = [starting_with_number]
                for current, val in enumerate(new_row[1:]):
                    if current > 11:
                        break
                    if "rd" not in val and val != "":
                        val = val.strip()
                        if val == "nam":
                            val = choice(["nam", "nữ"])
                        gen_data.append(questions.get(val, ""))
                        current += 1
                    elif val == "":
                        """
                        [ [0,1,2,3,current], [],[] ]
                        """
                        if "nam" in combinations[-1][current]:
                            gender = choice(["nam", "nữ"])
                            gen_data.append(gender)
                        else:
                            gen_data.append(combinations[-1][current])
                        current += 1
                    else:
                        # "rd" in the value
                        # remove "rd" in the name
                        new_val = val.replace("rd","").strip().split(",")
                        new_val = [int(number) for number in new_val]
                        gen_data.append(choice(new_val))
                        current += 1

                combinations.append(gen_data)
                number_generation += 1
        else:
            pass

    return combinations


def export2file(combinations):
    combinations.sort()
    unique_combination = list(k for k,_ in itertools.groupby(combinations))

    columns_name = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8_1_1', 'C8_1_2', 'C8_1_3',
           'C8_1_4','C8_1_5', 'C9_1']

    data_generated = pd.DataFrame(data=unique_combination, columns=columns_name)
    data_generated.astype(int)
    return data_generated

# data = """
# Assets:Bank:Car
# Assets:Bank:House
# Assets:Savings:Emergency
# Assets:Savings:Goals:Roof
# Assets:Reserved
# """
# J = []
#
# for line in data.split('\n'):
#     if not line: continue
#
#     # split the line into parts, start at the root list
#     # is there a dict here for this part?
#     #   yes? cool, dive into it for the next loop iteration
#     #   no? add one, with a list, ready for the next loop iteration
#     #    (unless we're at the final part, then stick it in the list
#     #     we made/found in the previous loop iteration)
#
#     parts = line.split(':')
#     parent_list, current_list = J, J
#
#     for index, part in enumerate(parts):
#         for item in current_list:
#             if part in item:
#                 parent_list, current_list = current_list, item[part]
#                 break
#         else:
#             if index == len(parts) - 1:
#                 # leaf node, add part as string
#                 current_list.append(part)
#             else:
#                 new_list = []
#                 current_list.append({part:new_list})
#                 parent_list, current_list = current_list, new_list
#
# print(J)

