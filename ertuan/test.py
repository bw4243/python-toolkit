#!/usr/bin/python
# -*-coding:utf-8-*-

import rsa

# pub_key_content = b'-----BEGIN RSA PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDMr60xVXiHxBm8CGTaGsRk5pTi\nJ0aC96EMBcw2jO2t32et1kFHSBHa/UuNLlO9dRcyLOaESfDMj3SI2iWpLvKItu3r\nwFopkBaSfXuD7iJvbJj/G+g9Y9dO5MjzQfBJ0+Z9eMyeAwBdMDniuZ22rLJDT7CH\nIe45N5FU/wg/vLv4kQIDAQAB\n-----END RSA PUBLIC KEY-----'
pub_key = rsa.PublicKey.load_pkcs1(open('public.pem').read())
#
ss = rsa.encrypt('acdSDFSDFZEEEEFFFLLMJSDKFSHKDFHSJDKFSHDF', pub_key)
print(ss)




# rsa.decrypt()



# # 先生成一对密钥，然后保存.pem格式文件，当然也可以直接使用
# (pubkey, privkey) = rsa.newkeys(1024)
#
# pub = pubkey.save_pkcs1()
# pubfile = open('public.pem','w+')
# pubfile.write(pub)
# pubfile.close()