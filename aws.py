import boto3

def get_location_by_text(query: str):
    client = boto3.client('location')
    response = client.search_place_index_for_text(
        IndexName='ecosensor-ws',
        Text=query,
        MaxResults=1,
        Language='it',
        Key="v1.public.eyJqdGkiOiI5ZTRlMjI0YS04YzFjLTQ0ZTctYTNlNC0xYTU0MDE4MGZjODYifW-qboxzpcYtKr-j4fVqbbFCawr3HZi4jw_jWFY2EQnam2o4pO5yR507FYYe7d8SflW8WX3gtWMRxyAnyzNkVyN0kdfLLKp1hbFpWS_oobYJJao-ubA09PZWprvV4LTo4LiZ6_GoH1DMRRKc30riprksGzAh9FSzy8UrOvJJ7FQppvI5n4J1iGRVz8EC0yue92wG7slKbx09kOYs006jLB4AMPYV-AGhzc3TPiEZ8ezEC7yMPzRZn17j31Ud7qHFPSbmqcLLpFy4d1qJSIjMPvdsOUF8QXmdjFvuhRgtQnaR8KGQI3Z-2rbZYwesgQ0P5dXhT8Ed3x5_Y-EqMAcBA40.ZWU0ZWIzMTktMWRhNi00Mzg0LTllMzYtNzlmMDU3MjRmYTkx"
    )
    if len(response['Results']) > 0:
        return response['Results'][0]['Place']
    return None

def get_location(lat: float, lng: float):
    """
    Asynchronously retrieves the location information for the given latitude and longitude.
    Info: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/client/search_place_index_for_position.html

    Args:
        lat (float): The latitude of the location.
        lng (float): The longitude of the location.

    Returns:
        dict: The response from the AWS Location Service containing the location information.

    Raises:
        botocore.exceptions.BotoCoreError: If there is an error with the AWS SDK.
        botocore.exceptions.ClientError: If there is an error with the AWS service.
    """
    client = boto3.client('location')
    response = client.search_place_index_for_position(
        IndexName='ecosensor-ws',
        Position=[
            lng,
            lat
        ],
        MaxResults=1,
        Language='it',
        Key="v1.public.eyJqdGkiOiI5ZTRlMjI0YS04YzFjLTQ0ZTctYTNlNC0xYTU0MDE4MGZjODYifW-qboxzpcYtKr-j4fVqbbFCawr3HZi4jw_jWFY2EQnam2o4pO5yR507FYYe7d8SflW8WX3gtWMRxyAnyzNkVyN0kdfLLKp1hbFpWS_oobYJJao-ubA09PZWprvV4LTo4LiZ6_GoH1DMRRKc30riprksGzAh9FSzy8UrOvJJ7FQppvI5n4J1iGRVz8EC0yue92wG7slKbx09kOYs006jLB4AMPYV-AGhzc3TPiEZ8ezEC7yMPzRZn17j31Ud7qHFPSbmqcLLpFy4d1qJSIjMPvdsOUF8QXmdjFvuhRgtQnaR8KGQI3Z-2rbZYwesgQ0P5dXhT8Ed3x5_Y-EqMAcBA40.ZWU0ZWIzMTktMWRhNi00Mzg0LTllMzYtNzlmMDU3MjRmYTkx"
    )
    if len(response['Results']) > 0:
        return response['Results'][0]['Place']
    return None