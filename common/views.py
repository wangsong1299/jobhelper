from django.shortcuts import render

# Create your views here.
from utils import CMpConn

if __name__ == "__main__":
	a=CMpConn()
	token=a.mpGetAccessToken()
	users=a.mpUserListGet()
	openids=users['data']['openid']
	for openid in openids:
		print a.mpUserInfoGet(openid)['nickname']

