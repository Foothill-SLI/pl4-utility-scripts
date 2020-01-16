import pandas
import sys

MAX_MATCH_SEC_DIFF = 2


def get_matched(export_list, manual_list):
    export_list.dropna(inplace=True)
    manual_list.dropna(inplace=True)

    export_i = 0
    manual_i = 0
    common_i = 0
    export_matched_list = pandas.Series()
    manual_matched_list = pandas.Series()

    while export_i < len(export_list) and manual_i < len(manual_list):
        # matches
        if abs(export_list[export_i] - manual_list[manual_i]) < MAX_MATCH_SEC_DIFF:
            export_matched_list.at[common_i] = export_list[export_i]
            manual_matched_list.at[common_i] = manual_list[manual_i]
            export_i += 1
            manual_i += 1
        # doesn't match
        elif export_list[export_i] < manual_list[manual_i]:
            export_matched_list.at[common_i] = export_list[export_i]
            manual_matched_list.at[common_i] = "NON EXIST"
            export_i += 1
        else:
            export_matched_list.at[common_i] = "MISSING"
            manual_matched_list.at[common_i] = manual_list[manual_i]
            manual_i += 1

        common_i += 1

    # add remaining
    export_matched_list = export_matched_list.append(export_list[export_i:], ignore_index=True)
    manual_matched_list = manual_matched_list.append(manual_list[manual_i:], ignore_index=True)

    result = pandas.DataFrame()
    result["exported"] = export_matched_list
    result["manual"] = manual_matched_list
    return result


# just an example for now, will probably make a "main" wrap later
camlytics_export_csv = pandas.read_csv(sys.argv[1])
manual_csv = pandas.read_csv(sys.argv[2])

# filter camlytics data
vehicle_only = camlytics_export_csv[camlytics_export_csv["Origin"] == "Vehicle"]
enter_times = vehicle_only[vehicle_only["Source name"] == "Enter"]["Timestamp"]
exit_times = vehicle_only[vehicle_only["Source name"] == "Exit"]["Timestamp"]

get_matched(enter_times.reset_index(drop=True), manual_csv["in"]).to_csv("matched_in.csv")
get_matched(exit_times.reset_index(drop=True), manual_csv["out"]).to_csv("matched_out.csv")
