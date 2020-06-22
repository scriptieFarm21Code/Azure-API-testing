Deze bestanden zijn gebruikt om een getrainde Azure API te testen.

Vanuit prediction.py werd er een script gedraaid om toekomstige waarde op te halen vanuit de de DB en ook de waarheid van de lezing. Hierna wordt requestNN.py aangesproken om een call te doen naar azure met de waarde en de voorspellingen worden opgehaald. En in anylitics haal ik alle waarde op en transformeer ik alles naar grafieken om te kijken hoe de voorspelling eruit ziet en hoeveel er klopt.
