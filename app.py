import azure.functions as func
import json
import math

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="CalculateArea", methods=["POST", "OPTIONS"])
def CalculateArea(req: func.HttpRequest) -> func.HttpResponse:
    # Tarayıcıların güvenlik için attığı ön istekleri (OPTIONS) doğrudan onayla
    if req.method == "OPTIONS":
        return func.HttpResponse(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        )

    try:
        body = req.get_json()
        shape = body.get("shape")
        v1 = float(body.get("value1", 0))
        v2 = float(body.get("value2", 0))

        if shape == "circle":
            result = math.pi * v1 * v1
        elif shape == "rectangle":
            result = v1 * v2
        elif shape == "triangle":
            result = 0.5 * v1 * v2
        else:
            return func.HttpResponse(
                json.dumps({"error": "Unknown shape"}),
                status_code=400,
                mimetype="application/json",
                headers={"Access-Control-Allow-Origin": "*"}
            )

        return func.HttpResponse(
            json.dumps({"result": result}),
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"}
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"}
        )