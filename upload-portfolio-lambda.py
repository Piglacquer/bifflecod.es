import boto3
import StringIO
from botocore.client import Config
import zipfile



def lambda_handler(event, context):
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
    return 'hello from LAMBDA'
