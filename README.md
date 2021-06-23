# RC-ECA-110
### Exploració de l'ús de la regla 110 dels Autòmates Cel·lulars Elementals com a reservoir en problemes de classificació

En aquest treball es vol investigar si els autòmats cel·lulars elemetals (regla 110) són capaços de servir com a reservoir en sistemes de reservoir computing dedicats a problemes de classificació, posant èmfasi en el benchmark estàndard MNIST.

Aquest repositori està el codi pel desenvolupament del TFG de l'estudiant Ferran Esteban juntament amb el seu director Jordi Delgado.

A la carpeta **implementació** es pot trobar el codi separat en les 2 branques que s'han dut a terme durant el procés: el problema del 5 bit i el benchmark del MNIST. Per dur a terme tot el codi s'ha utilitzat el llenguatge python 3.9.

- fivebitproblem
- mnistproblem

El **fivebit** problem conté els fitxers pythons per dur a terme el problema del 5 bit. Per poder executar el sistema calen tenir instal·lat els mòduls **Numpy** i **Sklearn**.

Primerament conté un generador dels 32 casos possibles
> generadorFiveBitProblem.py

i despres els 2 fitxers important.
> main.py
> reca.py

El main serveix per passar-li els hiperparàmetres del sistema. Els hiperparàmetres corresponents són: *I* (iteracions), *R* (mapeig aleatori), *bucle* (quantes vegades s'executa el sistema) i *predictor* (quantitat de predictors que tindrà el 5 bit. Un exemple d'execució seria:

> python main.py -I 8 -R 4 -b 50 -t 50

En aquest exemple es té 50 execucions amb un predictor de 50 on és maparà 4 vegades de manera aleatòria i l'autòmat s'executarà 8 vegades per cada input del sistema.

El **mnistproblem** conté els fitxers python per dur a terme el benchmark del MNIST. poder executar el sistema calen tenir instal·lat els mòduls **Numpy**, **Keras** i **Tensorflow**.
> mnistDataset.py

El mnistDataset és un generador del MNIST dataset utilitzant la llibreria de tensorflow d'on es descarreguen els fitxers en format Numpy. Aquest fitxers es guardaran directament a la carpeta *mnist_array*.

> mnistLayersGenerators.py

El mnistLayersGenerators.py únicament serveix per transformar cada matriu de 28x28 en 8 matrius de 28x28 ja que lalgorisme utilitzat cal tenir cada bit independent un de l'altre i com són 60.000 i 10.000 imatges (el training i el test respectivament) és més òptim pre calcular les matrius i guardar-les en fitxers numpy en una carpeta anomenada: *images_layers_generated*.
> mnistProblem.py

El mnist problem llegeix les matrius generades en el generator i dur a terme tot l'algorisme principal fins aconseguir un vector de 196*I on *I* és l'hiperparàmetre per decidir quantes vegades s'executarà l'autòmat i *f* servirà per decidir si s'escolleix els fitxers del training, els del test o si es vol obtenir el cas base on I=0. els casos de *f* són: "training" i  "test". Si *I* és 0 aleshores s'executarà el cas base.  Un exemple seria:
> python mnistProblem.py -I 10 -f "training"

els 2 últims fitxers són l'excel i el training.
> excel.py
> training.py

L'excel és un script per executar cada un dels 5 optimitzadors escollits (Adam, Nadam, Adamax, SGD i RMSprop) 10 vegades i guardar directament tots els valors en files i columnes d'un arxiu excel. Per poder executar-lo cal instal·lar els mòduls **xlwt** i el **Numpy**.

El training es dur a terme tots els càlculs de la xarxa neuronal amb els paràmetres rebuts de l'escript de l'excel utilitzant el mòdul (que cal instal·lar) de tensorflow. L'execució calcula tots els casos, per tant no té cap hiper paràmetre.
> python excel.py
