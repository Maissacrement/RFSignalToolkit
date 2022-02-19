from googletrans import Translator

trs = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])
print(trs.translate('test'))