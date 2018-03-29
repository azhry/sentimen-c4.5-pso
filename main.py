# -*- coding: utf-8 -*-
from helpers.Preprocessor import stemming, tokenizing, stopword_removal

text = "Susah cari driver sampai kepanasan dan kelaparan. Katanya pada demo masalah tarifnya diturunin. Kasian dong drivernya. Mereka sangat membantu kami. Tak pernah mengeluh walaupun kadang panas ataupun hujan tetap setia mengantar kami. Dan mereka sangat sopan terhadap kami dibandingkan vendor lain. Saya kira pendapatan 4rb rupiah tidak sebanding dengan perjuangan mereka bertaruh nyawa. Harusnya direspon perjuangan mereka hari ini. Biar kami juga dapat terbantu"
preprocessed = stemming(text)
preprocessed = tokenizing(preprocessed)
preprocessed = stopword_removal(preprocessed)
print(preprocessed)