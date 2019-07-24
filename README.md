# Custom Nano Service for IQ Bot and RPA

small Flask based Rest Services for IQ Bot and RPA

* Convert IQ Bot CSV output into a particular JSON format for Exceptions in Contracts

## Requirements

* python 3.7+

## Install

pip install Flask

## Run

On Mac / Linux / Unix: run the SERVICE_CSVToJson.sh
On Windows: run the SERVICE_CSVToJson.bat

## Endpoint

URL: http://127.0.0.1:5007/convert

Type: POST

Body Type: JSON

Body Example:

{
	"input_file":"/Users/bren/Documents/csvs/Medium/[3629f12d-43ea-46a0-9ec1-0d2f89485b8e]_M3_1.pdf.csv",
	"exception_column":2
}
