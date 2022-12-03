import datetime
import azure.functions as func
from azure.functions import AuthLevel
import logging

app = func.FunctionApp(http_auth_level=AuthLevel.ANONYMOUS)

@app.function_name(name="HTTPTrigger1")
@app.route(route="hello", auth_level=AuthLevel.FUNCTION)
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )

@app.function_name(name='echo')
@app.route(route="echo", auth_level=AuthLevel.ANONYMOUS)
def echo(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Echo function: recieve a request')

    return func.HttpResponse(
        'Success',
        status_code=200
    )

@app.function_name(name='process')
@app.route(route="process", auth_level=AuthLevel.ANONYMOUS)
def process(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Process function: recieve a request')

    return func.HttpResponse(
        'Success',
        status_code=200
    )

@app.function_name(name="mytimer")
@app.schedule(schedule="0 */5 * * * *", arg_name="mytimer", run_on_startup=True,
              use_monitor=False) 
def timer_function(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)


@app.function_name(name="getDataContent")
@app.route(route="data")
@app.blob_input('filepath', 'content/DxDiag.txt', connection='AzureWebJobsStorage')
def get_data_content(req: func.HttpRequest, filepath) -> func.HttpResponse:
    logging.info('Get Data Content Function: Receive a request')
    logging.info(filepath)
    if filepath:
        return func.HttpResponse(
            filepath.read(),
            status_code=200
        )
    else:
        return func.HttpResponse(
            status_code=404
        )
