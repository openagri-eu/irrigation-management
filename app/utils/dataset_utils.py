from schemas import Dataset as DatasetScheme

def min_max_date(dataset: list[DatasetScheme]):
    min_date = min(dataset, key=lambda d: d.date)
    max_date = max(dataset, key=lambda d: d.date)
    return [min_date, max_date]


def detect_irrigation_events(dataset: list[DatasetScheme]):
    const_threshold = 0.01
    increase_threshold = 0.05
    const_time = 4
    events = 0
    sorted_dataset = sorted(dataset, key=lambda d: d.date)

    start_index = None
    moisture = None

    for i in range(1, len(sorted_dataset)):
        prev = sorted_dataset[i - 1]
        curr = sorted_dataset[i]

        prev_moisture = (prev.soil_moisture_10 + prev.soil_moisture_20 + prev.soil_moisture_30 +
                         prev.soil_moisture_40 + prev.soil_moisture_50 + prev.soil_moisture_60) / 6
        curr_moisture = (curr.soil_moisture_10 + curr.soil_moisture_20 + curr.soil_moisture_30 +
                         curr.soil_moisture_40 + curr.soil_moisture_50 + curr.soil_moisture_60) / 6

        if moisture is None or (
                abs(curr_moisture - moisture) / moisture <= const_threshold and prev.rain == 0):
            if start_index is None:
                start_index = i - 1
            moisture = prev_moisture
        else:
            if start_index is not None and i - start_index >= const_time:
                const_period_no_rain = all(sorted_dataset[j].rain == 0 for j in range(start_index, i))

                if const_period_no_rain and (
                        curr_moisture - moisture) / moisture >= increase_threshold and curr.rain == 0:
                    events += 1

            start_index = None
            moisture = None

    return events


def count_precipitation_events(dataset: list[DatasetScheme]):
    increase_threshold = 0.05
    sorted_dataset = sorted(dataset, key=lambda d: d.date)

    event_count = 0
    in_event = False

    for i in range(1, len(sorted_dataset)):
        prev = sorted_dataset[i - 1]
        curr = sorted_dataset[i]

        prev_moisture = (prev.soil_moisture_10 + prev.soil_moisture_20 + prev.soil_moisture_30 +
                         prev.soil_moisture_40 + prev.soil_moisture_50 + prev.soil_moisture_60) / 6
        curr_moisture = (curr.soil_moisture_10 + curr.soil_moisture_20 + curr.soil_moisture_30 +
                         curr.soil_moisture_40 + curr.soil_moisture_50 + curr.soil_moisture_60) / 6

        if curr.rain == 0:
            if curr_moisture > prev_moisture and (curr_moisture - prev_moisture) / prev_moisture >= increase_threshold:
                if not in_event:
                    in_event = True

            elif curr_moisture == prev_moisture and in_event:
                continue
            else:
                if in_event:
                    event_count += 1
                in_event = False
        else:
            if in_event:
                event_count += 1
            in_event = False

    if in_event:
        event_count += 1

    return event_count


def count_high_dose_irrigation_events(dataset: list[DatasetScheme]):
    # TODO: check with the team
    high_dose_threshold = 0.10

    sorted_dataset = sorted(dataset, key=lambda d: d.date)

    irrigation_event_count = 0

    for i in range(1, len(sorted_dataset)):
        prev = sorted_dataset[i - 1]
        curr = sorted_dataset[i]

        # Calculate average soil moisture for both days
        prev_moisture = (prev.soil_moisture_10 + prev.soil_moisture_20 + prev.soil_moisture_30 +
                         prev.soil_moisture_40 + prev.soil_moisture_50 + prev.soil_moisture_60) / 6
        curr_moisture = (curr.soil_moisture_10 + curr.soil_moisture_20 + curr.soil_moisture_30 +
                         curr.soil_moisture_40 + curr.soil_moisture_50 + curr.soil_moisture_60) / 6

        if curr.rain == 0:
            if curr_moisture > prev_moisture and (curr_moisture - prev_moisture) / prev_moisture >= high_dose_threshold:
                irrigation_event_count += 1

    return irrigation_event_count


def get_high_dose_irrigation_events_dates(dataset: list[DatasetScheme]):
    # TODO: check with the team
    high_dose_threshold = 0.10

    sorted_dataset = sorted(dataset, key=lambda d: d.date)

    event_dates = []

    for i in range(1, len(sorted_dataset)):
        prev = sorted_dataset[i - 1]
        curr = sorted_dataset[i]

        prev_moisture = (prev.soil_moisture_10 + prev.soil_moisture_20 + prev.soil_moisture_30 +
                         prev.soil_moisture_40 + prev.soil_moisture_50 + prev.soil_moisture_60) / 6
        curr_moisture = (curr.soil_moisture_10 + curr.soil_moisture_20 + curr.soil_moisture_30 +
                         curr.soil_moisture_40 + curr.soil_moisture_50 + curr.soil_moisture_60) / 6

        if curr.rain == 0:
            if curr_moisture > prev_moisture and (curr_moisture - prev_moisture) / prev_moisture >= high_dose_threshold:
                event_dates.append(curr.date)

    return event_dates


def calculate_field_capacity(dataset: list[DatasetScheme]):
    sorted_dataset = sorted(dataset, key=lambda x: x.date)

    field_capacity = {
        10: None,
        20: None,
        30: None,
        40: None
    }

    for i in range(len(sorted_dataset)):
        curr = sorted_dataset[i]

        if curr.rain > 0:
            for j in range(i + 1, len(sorted_dataset)):
                next_itt = sorted_dataset[j]

                if next_itt.rain > 0:
                    break

                moisture_10 = next_itt.soil_moisture_10
                moisture_20 = next_itt.soil_moisture_20
                moisture_30 = next_itt.soil_moisture_30
                moisture_40 = next_itt.soil_moisture_40

                if field_capacity[10] is None or moisture_10 > field_capacity[10]:
                    field_capacity[10] = moisture_10
                if field_capacity[20] is None or moisture_20 > field_capacity[20]:
                    field_capacity[20] = moisture_20
                if field_capacity[30] is None or moisture_30 > field_capacity[30]:
                    field_capacity[30] = moisture_30
                if field_capacity[40] is None or moisture_40 > field_capacity[40]:
                    field_capacity[40] = moisture_40

    field_capacity_tuples = [(depth, value) for depth, value in field_capacity.items() if value is not None]

    return field_capacity_tuples


def calculate_stress_level(field_capacity_values):
    stress_level_tuples = [(depth, f"{float(value[:-1]) * 0.25}") for depth, value in field_capacity_values]

    return stress_level_tuples


def no_of_saturation_days(dataset: list[DatasetScheme], field_capacity_values):
    number_of_saturation_days = 0

    field_capacity_dict = {depth: float(value[:-1]) / 100 for depth, value in field_capacity_values}
    # TODO: check threshold
    for day in dataset:
        if (day.soil_moisture_10 >= field_capacity_dict[10] * 0.9 or
                day.soil_moisture_20 >= field_capacity_dict[20] * 0.9 or
                day.soil_moisture_30 >= field_capacity_dict[30] * 0.9 or
                day.soil_moisture_40 >= field_capacity_dict[40] * 0.9):
            number_of_saturation_days +=1

    return number_of_saturation_days


def get_saturation_dates(dataset: list[DatasetScheme], field_capacity_values):
    saturation_days = []

    field_capacity_dict = {depth: float(value[:-1]) / 100 for depth, value in field_capacity_values}

    for day in dataset:
        if (day.soil_moisture_10 >= field_capacity_dict[10] * 0.9 or
                day.soil_moisture_20 >= field_capacity_dict[20] * 0.9 or
                day.soil_moisture_30 >= field_capacity_dict[30] * 0.9 or
                day.soil_moisture_40 >= field_capacity_dict[40] * 0.9):
            saturation_days.append(day.date)

    return saturation_days


def get_stress_count(dataset: list[DatasetScheme], stress_level: list[[int, float]]):
    stress_ret = 0

    stress_level_dict = {depth: float(value) for depth, value in stress_level}

    for day in dataset:
        if (day.soil_moisture_10 < stress_level_dict.get(10, float('inf')) or
                day.soil_moisture_20 < stress_level_dict.get(20, float('inf')) or
                day.soil_moisture_30 < stress_level_dict.get(30, float('inf')) or
                day.soil_moisture_40 < stress_level_dict.get(40, float('inf'))):
            stress_ret += 1

    return stress_ret


def get_stress_dates(dataset: list[DatasetScheme], stress_level: list[[int, float]]):
    stress_dates = []

    stress_level_dict = {depth: float(value) for depth, value in stress_level}

    for day in dataset:
        if (day.soil_moisture_10 < stress_level_dict.get(10, float('inf')) or
                day.soil_moisture_20 < stress_level_dict.get(20, float('inf')) or
                day.soil_moisture_30 < stress_level_dict.get(30, float('inf')) or
                day.soil_moisture_40 < stress_level_dict.get(40, float('inf'))):
            stress_dates.append(day.date)

    return stress_dates