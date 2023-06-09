
# Analysis of electronic music channels on YouTube

This project extracts data from 4 major electronic music (Cercle, Boiler Room, Hor. Dj mag) channels using the Youtube API provided by Google cloud, those data are transformed
(using python and pandas) and uploaded daily to a S3 buckect via Lambdas, so it can be analyzed using Glue and Athena.




## Deployment

Get The Youtube API: 
To obtain access to Youtube API is needed an Google Cloud account. All the info related to de API in:

```bash
  https://developers.google.com/youtube/v3

```
In order to run the Lambda function its necessary:

    1.  Have a s3 bucket with the input csv file and another s3 for the output csv files

    2. Parameterize memory, ephemeral storage and scheme time (recommended 512mb,512mb,2 minutes respectively).

    3. Stablish the enviroment variables for "BUCKET_INPUT", "BUCKET_OUTPUT", "API_KEY" and "FILE_CHANNELS"
```bash
  curl -sSL install.astronomer.io | sudo bash -s 
```
After the lambda is funcional, stablish a EventBridge programmer with the periodicity expecified (daily). Once you have collected enough data in the S3 bucket, with AWS Glue generate the database using the crawler and analyze it through AWS Athena.



## Files

#### --youtube_data.ipynb :
File used to develop and test the functions that are applied in the lambda function.

#### --aws_lambda_function.py :
Script to execute on AWS Lambda.

#### --credentials.py :
File with the youtube API key, fill in this file with your key in case you want to run youtube_data.ipynb  .

