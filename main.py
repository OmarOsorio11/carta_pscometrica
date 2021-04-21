import numpy as np 
import matplotlib.pyplot as plt 


class Calcula:
    
    
    def calcula_presion_atmosferica_desde_altitud(self,altitud):
        presion_atmosferica=101.325*(1-(altitud)*2.25577*10**-5)**5.2559
        return presion_atmosferica
    

    def calcula_presion_de_vapor_saturacion(self,temperatura_celcius):
        temperatura_kelvines=temperatura_celcius+273.15
        a=np.array([[-5.6745359*10**3,
        6.3925247*10**0,
        -9.677643*10**-3,
        6.221570*10**-7,
        2.0747825*10**-9,
        -9.4844024*10**-13,
        4.1635019*10**0],
        [-5.8002206*10**3,
        1.3914993*10**0,
        -4.8640239*10**-2,
        4.1764768*10**-5,
        -1.4452093*10**-8,
        0.0,
        6.5459673*10**0]])

        if (temperatura_celcius>-100.0 and temperatura_celcius<0.0):
            aux=0
        elif (temperatura_celcius>0.0 and temperatura_celcius<200.0):
            aux=1
        else:
            print("Valores fuera de rango")
            return 0
        pvs1=a[aux,0]/temperatura_kelvines
        pvs2=a[aux,1]
        pvs3=a[aux,2]*temperatura_kelvines
        pvs4=a[aux,3]*temperatura_kelvines**2
        pvs5=a[aux,4]*temperatura_kelvines**3
        pvs6=a[aux,5]*temperatura_kelvines**4
        pvs7=a[aux,6]*np.log(temperatura_kelvines)
        pvs=pvs1+pvs2+pvs3+pvs4+pvs5+pvs6+pvs7
        return np.exp(pvs)


    def calcula_razon_de_humedad(self,humedar_relativa,presion_de_vapor_saturacion,presion_atmosferica):
        W=0.62198*((humedar_relativa*presion_de_vapor_saturacion)/(presion_atmosferica-humedar_relativa*presion_de_vapor_saturacion))
        return W
    
    
    def calcular_razon_de_humedad_saturacion (self,presion_de_vapor_saturacion,presion_atmosferica):
        Ws=0.62198*(presion_de_vapor_saturacion/(presion_atmosferica-presion_de_vapor_saturacion))
        return Ws      


    def calcular_saturacion_del_ire (self,razon_de_humedad,calcular_razon_de_humedad_saturacion):
        Sa=(razon_de_humedad/calcular_razon_de_humedad_saturacion)
        return Sa


    def calcula_volumen_especifico_aire_humedo (self,temperatura_celcius,razon_humedad,presion_atmosferica):
        temperatura_kelvines=temperatura_celcius+273.15
        Veh=((287.055*temperatura_kelvines)/presion_atmosferica)*((1+1.6078*razon_humedad)/(1+razon_humedad))
        return Veh


    def calcula_presion_de_vapor(self,presion_de_vapor_saturacion,humedar_relativa):
        Pv= humedar_relativa*presion_de_vapor_saturacion
        return Pv


    def calcula_razon_humedad_from_entalpia(self,entalpia,temperatura):
        Wa=(entalpia-1.006*temperatura)/(2501+1.805*temperatura)
        return Wa


    def calcula_razon_de_humedad_de_volumen_especifico(self,volumen_especifico,presion,temperatura):
        ra=287.055
        temperatura_kelvines=temperatura+273.15
        W=(((volumen_especifico*presion)/(ra*temperatura_kelvines))-1)/(1.6078)
        return W
    
    
    def calcula_entalpia(self,temperatura,razon_de_humedad):
        entalpia=1.006*temperatura+(2501+1.805*temperatura)*razon_de_humedad
        return entalpia


    def calcula_temperatura_punto_de_rocio(self,temperatura_bulbo_seco,presion_vapor):
        if (temperatura_bulbo_seco>-60 and temperatura_bulbo_seco<0):
            tprocio=-60.450+7.0322*(np.log(presion_vapor))+0.3700*(np.log(presion_vapor))**2
        elif (temperatura_bulbo_seco>=0 and temperatura_bulbo_seco<70):
            tprocio=-35.957-1.8726*(np.log(presion_vapor))+1.1681*(np.log(presion_vapor))**2
        else:
            print("Temperatura fuera de rangos")
            return 0
        return tprocio



class Grafica:
    def grafica_humedad_relativa(self,temperatura_bulbo_seco,humedad_relativa,presion,color):
        presion_de_vapor_saturacion=np.ones(len(temperatura_bulbo_seco))
        razon_de_humedad=np.ones(len(temperatura_bulbo_seco))
        index=0
        for temperatura in temperatura_bulbo_seco:
            presion_de_vapor_saturacion[index] = self.calcula.calcula_presion_de_vapor_saturacion(temperatura)
            razon_de_humedad[index]=self.calcula.calcula_razon_de_humedad(humedad_relativa,presion_de_vapor_saturacion[index],presion)
            index += 1
        plt.plot(temperatura_bulbo_seco,razon_de_humedad,color)


    def grafica_entalpia(self,temperatura_bulbo_seco,presion,entalpia,color):
        
        Wa=np.ones(len(temperatura_bulbo_seco))
        tbn=np.zeros(len(temperatura_bulbo_seco))
        index=0
        for temp in temperatura_bulbo_seco:
            pvs=self.calcula.calcula_presion_de_vapor_saturacion(temp) #Pa
            W=self.calcula.calcula_razon_de_humedad(1,pvs,presion)
            if self.calcula.calcula_razon_humedad_from_entalpia(entalpia,temp)<W:
                Wa[index]=self.calcula.calcula_razon_humedad_from_entalpia(entalpia,temp)
                tbn[index]=temp
                index+=1
        Wac=np.zeros(index)
        tbnc=np.zeros(index)
        for i in range(0,index):
            Wac[i]=Wa[i]
            tbnc[i]=tbn[i]
        plt.plot(tbnc,Wac,color)    

    def grafica_volumen_especifico(self,temperatura_bulbo_seco,volumen_especifico,presion,color):
        Wa=np.ones(len(temperatura_bulbo_seco))
        tbn=np.zeros(len(temperatura_bulbo_seco))
        index=0
        for temp in temperatura_bulbo_seco:
            w=self.calcula.calcula_razon_de_humedad_de_volumen_especifico(volumen_especifico,presion,temp)
            #pvs=self.calcula.calcula_presion_de_vapor_saturacion(temp) 
            if True:
                Wa[index]=w
                tbn[index]=temp
                index+=1
                Wac=np.zeros(index)
        tbnc=np.zeros(index)
        for i in range(0,index):
            Wac[i]=Wa[i]
            tbnc[i]=tbn[i]
        plt.plot(tbnc,Wac,color)


    def grafica_contenido_humedad(self,razon_humedad,color):
        plt.plot(np.arange(-10,60,0.001),np.full(len(np.arange(-10,60,0.001)),razon_humedad),color)


    def grafica_temperatura_bulbo_seco(self,temperatura,presion,color):
        pvsx=self.calcula.calcula_presion_de_vapor_saturacion(temperatura)
        limMax=self.calcula.calcula_razon_de_humedad(1,pvsx,presion)
        if (limMax>=0.03):
            limMax=0.03
        plt.plot(np.full(len(np.arange(0,(limMax+0.001),0.001)),temperatura),np.arange(0,(limMax+0.001),0.001),color)
    
    
    def grafica_Punto(self,data,presion,index):
        presion_vapor_de_saturacion=self.calcula.calcula_presion_de_vapor_saturacion(data[index,1])
        humedar_relativa=(data[index,0])/100
        wrazon=self.calcula.calcula_razon_de_humedad(humedar_relativa,presion_vapor_de_saturacion,presion)
        temp=float(data[index,1])
        plt.plot(temp,wrazon,marker="o",color='red')  


    def __init__(self):
        self.calcula=Calcula()


class Main:
    opc = -1

    def print_header(self):
        print("Bienvenido a tu carta Psicometrica\n")
        print("Selecciona una opcion: ")
        print("1) Calculos de valores:")
        print("2) Mostrar la carta psicometrica:")
        print("3) Mostrar la carta psicometrica, con datos de meses:")


    def print_opc(self):
        print("Seleccione el tipo de linea: ")
        print("1) Temperatura Bulbo Seco")
        print("2) Humedad Relativa")
        print("3) Entalpia")
        print("4) Volumen Especifico, aire seco")
        print("5) Razon de humedad")


    def grafica_lineas_extra(self,presion,temperatura_bulbo_seco):
        self.print_opc()
        tl_extra=int(input())
        if tl_extra==1:
            print("Ingrese la temperatura del bulbo seco: ")
            tempera=float(input())
            self.grafica.grafica_temperatura_bulbo_seco(tempera,presion,'r')
        if tl_extra==2:
            print("Ingrese la humedad relativa: ")
            HRx=float(input())
            color='r'
            self.grafica.grafica_humedad_relativa(temperatura_bulbo_seco,HRx,presion,color) 
        if tl_extra==3:
            print("Ingresa la entalpia: ")
            Ental=float(input())
            color='r'
            self.grafica.grafica_entalpia(temperatura_bulbo_seco,presion,Ental,color)
        if tl_extra==4:
            print("Ingresa el volumen especifico en aire seco ")
            ves=float(input())
            color='r'
            self.grafica.grafica_volumen_especifico(temperatura_bulbo_seco,ves,presion,color)
        if tl_extra==5:
            print("Ingresa el valor de la razon de humedad ")
            rhum=float(input())
            color='r'
            self.grafica.grafica_contenido_humedad(rhum,color)
    

    def get_altitud(self):
        print("Ingrese la altitud en metros sobre el nivel del mar: ")
        alt=float(input())
        return alt
    
    def calcual_datos(self,altitud):
        print("Ingrese la cantidad de datos a calcular: ")
        ctdatos=int(input())

        datosTBS=np.zeros(ctdatos)
        datosHR=np.zeros(ctdatos)
        pvs=np.zeros(ctdatos)
        pv=np.zeros(ctdatos)
        W=np.zeros(ctdatos)
        Ws=np.zeros(ctdatos)
        H=np.zeros(ctdatos)
        Veh=np.zeros(ctdatos)
        Tpr=np.zeros(ctdatos)
        Miu=np.zeros(ctdatos)
        
        for x in range(0,ctdatos):
            print("Ingrese la temperatura de bulbo seco para el dato ",(x+1))
            datosTBS[x]=float(input())
            print("Ingrese la humedad relativa para el dato ",(x+1))
            datosHR[x]=float(input())
        
        p=self.calcula.calcula_presion_atmosferica_desde_altitud(altitud)*1000
        for x in range(0,ctdatos):
            pvs[x]=self.calcula.calcula_presion_de_vapor_saturacion(datosTBS[x])
            pv[x]=self.calcula.calcula_presion_de_vapor(pvs[x],datosHR[x])
            W[x]=self.calcula.calcula_razon_de_humedad(datosHR[x],pvs[x],p)
            Ws[x]=self.calcula.calcular_razon_de_humedad_saturacion(pvs[x],p)
            H[x]=self.calcula.calcula_entalpia(datosTBS[x],W[x])
            Veh[x]=self.calcula.calcula_volumen_especifico_aire_humedo(datosTBS[x],W[x],p)
            Tpr[x]=self.calcula.calcula_temperatura_punto_de_rocio(datosTBS[x],pv[x])
            Miu[x]=self.calcula.calcular_saturacion_del_ire(W[x],Ws[x])
        print("Los Datos son:")
        print("Patm ",p)
        for x in range(0,ctdatos):
            print("Para el dato numero ",(x+1))
            print("Pws=",(pvs[x]))
            print("Pw=",(pv[x]))
            print("W=",(W[x]))
            print("Ws=",(Ws[x]))
            print("h=",(H[x]))
            print("Veh=",(Veh[x]))
            print("Tbs=",(datosTBS[x]))
            print("Tpr=",(Tpr[x]))
            print("HR=",(datosHR[x]))
            print("GSaturacion=",(Miu[x]))

    def grafica_carta(self,altitud):
        p=self.calcula.calcula_presion_atmosferica_desde_altitud(altitud)*1000
        #Variables de entrada
        tbs=np.arange(-10,61,0.1)
        tbsg=np.arange(-5,61,5)
        rhumedad=np.arange(0,0.030,0.005)
        entalpiasG=np.arange(-10,130,5)
        volumenesEspecificos=np.arange(0.75,2.05,0.05)
        Hrelativas=np.array([0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.90,1])
        #Graficar Humedad Relativa
        for HR in Hrelativas:
            color='c'
            self.grafica.grafica_humedad_relativa(tbs,HR,p,color)    
        #Grafica de Temperatura de bulbo seco 
        for x in tbsg:
            self.grafica.grafica_temperatura_bulbo_seco(x,p,'k')
        for x in rhumedad:
            self.grafica.grafica_contenido_humedad(x,'k')
        for x in entalpiasG:
            color='m'
            self.grafica.grafica_entalpia(tbs,p,x,color)
        #volumen especifico
        for vol in volumenesEspecificos:
            self.grafica.grafica_volumen_especifico(tbs,vol,p,'b')
        
        print("Deseas Agregar lineas, ingresa el numero, en caso contrario, ingresa 0")
        nmlExtras=int(input())
        if nmlExtras>1:
            for x in range(0,nmlExtras):
                self.grafica_lineas_extra(p,tbs)
        elif nmlExtras==1:
            self.grafica_lineas_extra(p,tbs)
        
    def grafica_datos_de_cvs(self,altitud):
        #para graficar datos de los datos
        #Primero abrimos los datos
        presion=self.calcula.calcula_presion_atmosferica_desde_altitud(altitud)*1000
        eneroData=np.loadtxt('enero.csv',dtype=float,delimiter=',',skiprows=0)
        febreroData=np.loadtxt('febrero.csv',dtype=float,delimiter=',',skiprows=0)
        marzoData=np.loadtxt('marzo.csv',dtype=float,delimiter=',',skiprows=0)
        sumaAA=0
        sumaBA=0
        sumaAB=0
        sumaBB=0
        sumaAC=0
        sumaBC=0
        
        for i in range(0,len(eneroData)):
            self.grafica.grafica_Punto(eneroData,presion,i) 
            #Promedios
            sumaAA=sumaAA+eneroData[i,0]
            sumaBA=sumaBA+eneroData[i,1]
        for i in range(0,len(febreroData)):
            self.grafica.grafica_Punto(febreroData,presion,i) 
            #Promedios
            sumaAB=sumaAB+febreroData[i,0]
            sumaBB=sumaBB+febreroData[i,1]
        for i in range(0,len(marzoData)):
            self.grafica.grafica_Punto(marzoData,presion,i) 
            #Promedios
            sumaAC=sumaAC+marzoData[i,0]
            sumaBC=sumaBC+marzoData[i,1]
        mediaAA=sumaAA/len(eneroData)
        mediaBA=sumaBA/len(eneroData)
        presionVaporSaturacionA=self.calcula.calcula_presion_de_vapor_saturacion(mediaBA)
        humedarRA=(mediaAA)/100
        wrazonA=self.calcula.calcula_razon_de_humedad(humedarRA,presionVaporSaturacionA,presion)
        tempA=float(mediaBA)
        plt.plot(tempA,wrazonA,marker="o",color='yellow')  
        
        mediaAB=sumaAB/len(eneroData)
        mediaBB=sumaBB/len(eneroData)
        presionVaporSaturacionB=self.calcula.calcula_presion_de_vapor_saturacion(mediaBB)
        humedarRB=(mediaAB)/100
        wrazonB=self.calcula.calcula_razon_de_humedad(humedarRB,presionVaporSaturacionB,presion)
        tempB=float(mediaBB)
        plt.plot(tempB,wrazonB,marker="o",color='yellow')  
        
        mediaAC=sumaAC/len(eneroData)
        mediaBC=sumaBC/len(eneroData)
        presionVaporSaturacionC=self.calcula.calcula_presion_de_vapor_saturacion(mediaBC)
        humedarRC=(mediaAC)/100
        wrazonC=self.calcula.calcula_razon_de_humedad(humedarRC,presionVaporSaturacionC,presion)
        tempC=float(mediaBC)
        plt.plot(tempC,wrazonA,marker="o",color='yellow')  

    def final(self):
        plt.xlim(-10,60)
        plt.xlabel("Temperatura Bulbo Seco")
        plt.ylim(0,0.025)
        plt.ylabel("Razon de humedad")
        plt.title("Carta Psicometrica")
        plt.show()


    def menu_principal(self,opcion):
        
        if opcion==1: 
            altitud=self.get_altitud()
            self.calcual_datos(altitud)

            
        elif (opcion==2):
            altitud=self.get_altitud()
            self.grafica_carta(altitud)
            self.final()

        elif (opcion==3):
            altitud=self.get_altitud()
            self.grafica_carta(altitud)
            self.grafica_datos_de_cvs(altitud)
            self.final()
            

    

    def __init__(self):
        self.calcula=Calcula()
        self.grafica=Grafica()
        self.print_header()
        self.opc=int(input())
        self.menu_principal(self.opc)




if __name__ == '__main__':
    princ=Main()
    
