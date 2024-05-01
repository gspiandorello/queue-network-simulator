import yaml


def readYamlFile(filePath):
    with open(filePath, 'r') as file:
        return yaml.safe_load(file)


def validateYamlFile(yamlData):
    generalParams = ['firstArrivalTime', 'quantityRandomNumbers', 'seed']
    for param in generalParams:
        if param not in yamlData:
            raise ValueError(f"Missing required config parameter: {param}")

        if param == 'quantityRandomNumbers' and not isinstance(yamlData[param], int):
            raise TypeError(f"'{param}' must be an integer, got {
                            type(yamlData[param])} instead.")
        if param == 'seed' and not isinstance(yamlData['seed'], int):
            raise TypeError(f"'seed' must be an integer, got {
                            type(yamlData['seed'])} instead.")

    if 'queueList' not in yamlData:
        raise ValueError("Missing 'queueList' in configuration.")
    queueData = yamlData['queueList']

    validateQueueData(queueData)


def validateQueueData(queueData):
    requiredFields = ['name', 'servers', 'minService', 'maxService']
    optionalFieldsWithDefaults = {
        'capacity': 999999,
        'minArrival': -1,
        'maxArrival': -1,
        'network': []
    }

    for queue in queueData:
        for field in requiredFields:
            if field not in queue:
                raise ValueError(f"Missing required field {
                                 field} in queue configuration.")

        if not isinstance(queue['servers'], int):
            raise TypeError(f"'servers' must be an int, got {
                            type(queue['servers'])} instead.")
        if not isinstance(queue['minService'], (int, float)):
            raise TypeError(f"'minService' must be a number, got {
                            type(queue['minService'])} instead.")
        if not isinstance(queue['maxService'], (int, float)):
            raise TypeError(f"'maxService' must be a number, got {
                            type(queue['maxService'])} instead.")

        for field, default_value in optionalFieldsWithDefaults.items():
            queue[field] = queue.get(field, default_value)

        for link in queue['network']:
            if 'target' not in link or 'probability' not in link:
                raise ValueError(
                    "Each network link must have 'target' and 'probability' keys.")
            if not isinstance(link['probability'], (int, float)):
                raise TypeError(f"Network 'probability' must be a number, got {
                                type(link['probability'])} instead.")
