import boto3
import StringIO
from botocore.client import Config
import zipfile

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-2:492894253452:deployPortfolioTopic')

    try:
        s3 = boto3.resource('s3')

        portfolio_bucket = s3.Bucket('portfolio.bifflecod.es')
        build_bucket = s3.Bucket('bifflecod.es.build')

        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('bifflecod-es.zip', portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm)
                portfolio_bucket.Object(nm).Acl().put(ACL = 'public-read')

        print 'job done!'

        topic.publish(Subject="Portfolio Deployed", Message="Portfolio deployed successfully!!!")
    except:
        topic.publish(Subject="Portfolio Deployment Failed", Message="Whoops, your deployment failed")
        raise
    return 'hello from LAMBDA'
