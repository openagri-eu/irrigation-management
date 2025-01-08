import utils
import uuid
from schemas import DatasetScheme, DatasetAnalysis, EToResponse

def jsonld_get_dataset(dataset: list[DatasetScheme]):
    context = utils.context
    graph = []

    uuid4_temp = uuid.uuid4()


    graph_elements = map(lambda dataset_scheme: {
        "@id": "urn:openagri:soilMoistureMonitoring:{}".format(uuid4_temp),
        "@type": ["ObservationCollection"],
        "description": "Monitoring of soil moisture levels at various depths in the soil of a parcel",
        "resultTime": "{}".format(dataset_scheme.date),
        "observedProperty": {
            "@id": "urn:openagri:Moisture:op:{}".format(uuid4_temp),
            "@type": ["ObservableProperty", "Moisture"],
            "name": "The moisture level in some material"
        },
        "hasFeatureOfInterest": {
            "@id": "urn:openagri:soil:foi:{}".format(uuid4_temp),
            "@type": ["FeatureOfInterest", "Soil"]
        },
        "precipitation": {
            "@id": "urn:openagri:precipitation:{}".format(dataset_scheme.rain),
            "@type": "https://smartdatamodels.org/dataModel.Weather/precipitation",
            "description": "the measured precipitation during monitoring of the soil moisture",
            "value": dataset_scheme.rain
        },
        "temperature": {
            "@id": "urn:openagri:temperature:{}".format(dataset_scheme.temperature),
            "@type": "https://smartdatamodels.org/dataModel.Weather/temperature",
            "description": "the measured temperature during monitoring of the soil moisture",
            "value": dataset_scheme.temperature
        },
        "relativeHumidity": {
            "@id": "urn:openagri:relativeHumidity:{}".format(dataset_scheme.humidity),
            "@type": "https://smartdatamodels.org/dataModel.Weather/relativeHumidity",
            "description": "the measured relative humidity during monitoring of the soil moisture",
            "value": dataset_scheme.humidity
        },
        "hasMember": [
            {
                "@id": "urn:openagri:soilMoistureVwc:obs1:{}".format(uuid4_temp),
                "@type": ["Observation"],
                "hasSimpleResult": "{}".format(dataset_scheme.soil_moisture_10),
                "atDepth": {
                    "@id": "urn:openagri:depth:10",
                    "@type": "[Measure]",
                    "hasNumericValue": "10",
                    "hasUnit": "om:centimetre"
                }
            },
            {
                "@id": "urn:openagri:soilMoistureVwc:obs2:{}".format(uuid4_temp),
                "@type": ["Observation"],
                "hasSimpleResult": "{}".format(dataset_scheme.soil_moisture_20),
                "atDepth": {
                    "@id": "urn:openagri:depth:20",
                    "@type": "[Measure]",
                    "hasNumericValue": "20",
                    "hasUnit": "om:centimetre"
                }
            },
            {
                "@id": "urn:openagri:soilMoistureVwc:obs3:{}".format(uuid4_temp),
                "@type": ["Observation"],
                "hasSimpleResult": "{}".format(dataset_scheme.soil_moisture_30),
                "atDepth": {
                    "@id": "urn:openagri:depth:30",
                    "@type": "[Measure]",
                    "hasNumericValue": "30",
                    "hasUnit": "om:centimetre"
                }
            },
            {
                "@id": "urn:openagri:soilMoistureVwc:obs4:{}".format(uuid4_temp),
                "@type": ["Observation"],
                "hasSimpleResult": "{}".format(dataset_scheme.soil_moisture_40),
                "atDepth": {
                    "@id": "urn:openagri:depth:40",
                    "@type": "[Measure]",
                    "hasNumericValue": "40",
                    "hasUnit": "om:centimetre"
                }
            },
            {
                "@id": "urn:openagri:soilMoistureVwc:obs5:{}".format(uuid4_temp),
                "@type": ["Observation"],
                "hasSimpleResult": "{}".format(dataset_scheme.soil_moisture_50),
                "atDepth": {
                    "@id": "urn:openagri:depth:50",
                    "@type": "[Measure]",
                    "hasNumericValue": "50",
                    "hasUnit": "om:centimetre"
                }
            },
            {
                "@id": "urn:openagri:soilMoistureVwc:obs6:{}".format(uuid4_temp),
                "@type": ["Observation"],
                "hasSimpleResult": "{}".format(dataset_scheme.soil_moisture_60),
                "atDepth": {
                    "@id": "urn:openagri:depth:60",
                    "@type": "[Measure]",
                    "hasNumericValue": "60",
                    "hasUnit": "om:centimetre"
                }
            }
        ]

    }, dataset)

    graph.append(graph_elements)

    doc = {
        "@context": context,
        "@graph": graph
    }
    return doc


def jsonld_analyse_soil_moisture(analysis: DatasetAnalysis):
    context = utils.context
    graph = []

    uuid4_temp = uuid.uuid4()

    high_dose_irrigation_events_dates = analysis.high_dose_irrigation_events_dates
    jsonld_high_dose_irrigation_events_dates = map(lambda date: {
                                                                    "@value": "{}".format(date),
					                                                "@type": "xsd:DateTime"
                                                                }, high_dose_irrigation_events_dates)

    saturation_dates = analysis.saturation_dates
    jsonld_saturation_dates = map(lambda date: {
                                                "@value": "{}".format(date),
                                                "@type": "xsd:DateTime"
                                                }, saturation_dates)

    stress_dates = analysis.stress_dates
    jsonld_stress_dates = map(lambda date: {
                                            "@value": "{}".format(date),
                                            "@type": "xsd:DateTime"
                                            }, stress_dates)

    field_capacity = analysis.field_capacity
    jsonld_field_capacity = map(lambda fc: {
        "@id": "urn:openagri:field:capacity:{}".format(uuid4_temp),
        "@type": "QuantityValue",
        "numericValue": fc(1),
        "unit": "om:Percentage",
        "atDepth": {
            "@id": "urn:openagri:depth:{}".format(fc(0)),
            "@type": "Measure",
            "hasNumericValue": "{}".format(fc(0)),
            "hasUnit": "om:centimetre"
        }
    }, field_capacity)

    stress_level = analysis.stress_level
    jsonld_stress_level = map(lambda sl: {
        "@id": "urn:openagri:stress:level:{}".format(uuid4_temp),
        "@type": "QuantityValue",
        "numericValue": sl(1),
        "unit": "om:Percentage",
        "atDepth": {
            "@id": "urn:openagri:depth:{}".format(sl(0)),
            "@type": "Measure",
            "hasNumericValue": "{}".format(sl(0)),
            "hasUnit": "om:centimetre"
        }
    }, stress_level)

    graph_elements = {
        "@id": "urn:openagri:soilMoistureAggregation:{}".format(uuid4_temp),
        "@type": "SoilMoistureAggregation",
        "description": "Aggregation of soil moisture levels over a longer period including saturation, irrigation and stress indications",
		"duringPeriod": {
			"@id": "urn:openagri:Period:{}".format(uuid4_temp),
			"@type": "Interval",
			"hasBeginning": {
				"@id": "urn:openagri:Instant:{}".format(uuid4_temp),
				"@type": "Instant",
				"inXSDDateTime": "{}".format(analysis.time_period[0])
			},
			"hasEnd": {
				"@id": "urn:openagri:Instant:".format(uuid4_temp),
				"@type": "Instant",
				"inXSDDateTime": "{}".format(analysis.time_period[-1])
			}
		},
		"numberOfPrecipitationEvents": analysis.precipitation_events,
		"saturationAnalysis": {
			"@id": "urn:openagri:Analysis:{}".format(uuid4_temp),
			"@type": "SaturationAnalysis",
			"numberOfSaturationDays": analysis.number_of_saturation_days,
			"hasSaturationDates": [
                jsonld_saturation_dates
			],
			"hasFieldCapacities": [
                jsonld_field_capacity
			]
		},
		"stressAnalysis": {
			"@id": "urn:openagri:Analysis:{}".format(uuid4_temp),
			"@type": "StressAnalysis",
			"numberOfStressDays": analysis.no_of_stress_days,
			"hasStressDates": [
                jsonld_stress_dates
			],
			"hasStressLevels": [
                jsonld_stress_level
			]
		},
		"irrigationAnalysis": {
			"@id": "urn:openagri:Analysis:{}".format(uuid4_temp),
			"@type": "IrrigationAnalysis",
			"numberOfIrrigationOperations": analysis.irrigation_events_detected,
			"numberOfHighDoseIrrigationOperations": analysis.high_dose_irrigation_events,
			"hasHighDoseIrrigationOperationDates": [
				jsonld_high_dose_irrigation_events_dates
			]
		}
    }

    graph.append(graph_elements)

    doc = {
        "@context": context,
        "@graph": graph
    }
    return doc


def jsonld_eto_response(eto: EToResponse):
    context = utils.context
    graph = []

    uuid4_temp = uuid.uuid4()

    calculations = eto.calculations

    graph_elements = map(lambda c: {
        "@id": "urn:openagri:evaporation:calculation:{}".format(uuid4_temp),
        "@type": "Observation",
        "description": "Measurement or calculation of the evaporation of the soil on a parcel on a specific date",
        "resultTime": "{}".format(c.date),
        "observedProperty": {
            "@id": "urn:openagri:evaporation:op:{}".format(uuid4_temp),
            "@type": ["ObservableProperty", "Evaporation"]
        },
        "hasFeatureOfInterest": {
            "@id": "urn:openagri:soil:foi:{}".format(uuid4_temp),
            "@type": ["FeatureOfInterest", "Soil"]
        },
        "hasSimpleResult": "{}".format(c.value)
    }, calculations)

    graph.append(graph_elements)

    doc = {
        "@context": context,
        "@graph": graph
    }
    return doc