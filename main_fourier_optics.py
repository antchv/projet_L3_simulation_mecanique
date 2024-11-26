# -*- coding: utf-8 -*-

from tkinter import *
import tkinter as tk
# Import des bibliotheques necessaire
import pylab as plb
import matplotlib.image as mpimg


# Import de l'image a traiter ( en png )
image = mpimg.imread("oiseau.png")


# Definition des axes x et y
axe_x = image.shape[0]
axe_y = image.shape[1]


# Transformee de Fourier de l'image grace a la fonction fft (fast fourier transform)
imagefft=plb.zeros((axe_x,axe_y,3),dtype=plb.complex64)
for i in range(3):
    imagefft[:,:,i]=plb.fftshift(plb.fft2(image[:,:,i])) 
    #la fonction fftshift permet de placer la frequence nulle au centre

    
#copie de la fft de l'image pour pouvoir la filtree par la 
#suite en gardant la fft non fitree afin de les comparer

imagefft_filtre1=plb.copy(imagefft)
imagefft_filtre2=plb.copy(imagefft) 


###Definition des filtres 

def filtrage_passe_bas (imagefft_filtre, diaphragme):
    # Filtre passe-bas donc on coupe les hautes frequences, comme un diaphragme 
    
    # Tableau de booleen aux memes dimension que l'image, un booleen par pixel
    Passe_Bas=plb.zeros((axe_x,axe_y),dtype=bool)
    
    # On remplit la liste passe-bas
    for i in range(axe_x):
        for j in range(axe_y):
            Passe_Bas[i,j]=( (i-axe_x/2)**2 + (j-axe_y/2)**2 > axe_x*axe_y/
            diaphragme) 
            #le booleen vaut true si la condition est verifier est donc l'amplitude est coupee

    # On coupe quand le booleen vaut True
    imagefft_filtre[Passe_Bas]=[0,0,0]
    
    # Transformee de Fourier inverse pour avoir notre image modifiee
    imageinv=plb.zeros((axe_x,axe_y,3),dtype=plb.float32)
    for i in range(3):
        imageinv[:,:,i]=plb.ifft2(plb.ifftshift(imagefft_filtre[:,:,i]))
    
    # On recupere nos images 
    return imagefft_filtre,imageinv


def filtrage_passe_haut (imagefft_filtre, cache):
    # Filtre passe-haut donc on coupe les basses frequences, comme une pastille opaque 
    
    # Tableau de booleen aux memes dimension que l'image, un booleen par pixel
    Passe_Haut=plb.zeros((axe_x,axe_y),dtype=bool)
    
    # On remplit la liste passe-haut
    for i in range(axe_x):
        for j in range(axe_y):
            Passe_Haut[i,j]=( (i-axe_x/2)**2 + (j-axe_y/2)**2 < axe_x*axe_y/cache) 
            #le booleen vaut true si la condition est verifier est donc l'amplitude est coupee

    # On coupe quand le booleen vaut True
    imagefft_filtre[Passe_Haut]=[0,0,0]
    
    # Transformee de Fourier inverse pour avoir notre image modifiee
    imageinv=plb.zeros((axe_x,axe_y,3),dtype=plb.float32)
    for i in range(3):
        imageinv[:,:,i]=plb.ifft2(plb.ifftshift(imagefft_filtre[:,:,i]))
    
    # On recupere nos images
    return imagefft_filtre,imageinv




# Fonction pour recalculer et afficher la figure a chaque lancement
# Uniquement pour le filtre passe-bas et passe-haut donc detramage et tramage de l'image

def calcul():
    # On ferme la figure du lancement precedent
    plb.close()
    
    # On recupere les valeurs des curseurs
    diaphragme=curseur_diaphragme.get()
    cache=curseur_cache.get()
    
    # Import de l'image a traiter ( en png )
    image = mpimg.imread("oiseau.png")
    
    
    # Definition des axes x et y
    axe_x = image.shape[0]
    axe_y = image.shape[1]
    
    
    # Transformee de Fourier de l'image grace a la fonction fft ( fast fourier transform )
    imagefft=plb.zeros((axe_x,axe_y,3),dtype=plb.complex64)
    for i in range(3):
        imagefft[:,:,i]=plb.fftshift(plb.fft2(image[:,:,i])) 
        #la fonction fftshift permet de placer la frequence nulle au centre
    
    # On creer deux copie, une pour chaque filtrage
    imagefft_filtre1=plb.copy(imagefft)
    imagefft_filtre2=plb.copy(imagefft) 


    ### Filtre passe-bas donc on coupe les hautes frequences ( comme un diaphragme )
    Passe_Bas=plb.zeros((axe_x,axe_y),dtype=bool)
    
    # On remplit la liste passe-bas
    for i in range(axe_x):
        for j in range(axe_y):
            Passe_Bas[i,j]=( (i-axe_x/2)**2 + (j-axe_y/2)**2 > 
            
            axe_x*axe_y/diaphragme) 
            
            #le booleen vaut true si la condition est verifier est donc l'amplitude est coupee

    # On applique le filtre donc met a zeros les valeurs correspondantes
    imagefft_filtre1[Passe_Bas]=[0,0,0]
    
    # Transformee de Fourier inverse pour avoir notre image modifiee
    imageinv=plb.zeros((axe_x,axe_y,3),dtype=plb.float32)
    for i in range(3):
        imageinv[:,:,i]=plb.real(plb.ifft2(plb.ifftshift(imagefft_filtre1[:,:,i])))
    
    
    
    
    ### Filtre passe-haut donc on coupe les basses frequences ( comme une pastille opaque )
    Passe_Haut=plb.zeros((axe_x,axe_y),dtype=bool)
    
    # On remplit la liste passe-haut
    for i in range(axe_x):
        for j in range(axe_y):
            Passe_Haut[i,j]=( (i-axe_x/2)**2 + (j-axe_y/2)**2 < axe_x*axe_y/cache) 
            
            #le booleen vaut true si la condition est verifier est donc l'amplitude est coupee

    
    imagefft_filtre2[Passe_Haut]=[0,0,0]
    
    # Transformee de Fourier inverse pour avoir notre image modifiee
    imageinv2=plb.zeros((axe_x,axe_y,3),dtype=plb.float32)
    for i in range(3):
        imageinv2[:,:,i]=plb.real(plb.ifft2(plb.ifftshift(imagefft_filtre2[:,:,i])))
   
    
    # Figure pour afficher les trois images et les trois plan de fourier
    # ( Non filtre, filtre passe-bas, filtre passe-haut )
    fig2=plb.figure(figsize=(10,10))
    
    axe21=fig2.add_subplot(231)
    axe21.imshow(image)
    axe21.set_title('image initiale')
    
    axe22=fig2.add_subplot(234)
    axe22.imshow(plb.log10(plb.absolute(imagefft[:,:,0])))
    axe22.set_title('transformée de Fourier non filtrée',fontsize=10)
    
 
    axe23=fig2.add_subplot(232)
    axe23.set_title('image détramée')
    axe23.imshow(imageinv)
    
    axe24=fig2.add_subplot(235)
    axe24.imshow(plb.log10(plb.absolute(imagefft_filtre1[:,:,0])))
    axe24.set_title('transformée de Fourier détramée',fontsize=10)
   

    axe25=fig2.add_subplot(233)
    axe25.set_title('image tramée')
    axe25.imshow(imageinv2)

    axe26=fig2.add_subplot(236)
    axe26.imshow(plb.log10(plb.absolute(imagefft_filtre2[:,:,0])))
    axe26.set_title('transformée de Fourier tramée',fontsize=10)

    plb.show()
 
   


# Creation de la fenetre principale
interface = tk.Tk()
interface.geometry("500x400")
interface.title("détramage et tramage d'une image")

# 1er curseur pour la taille du diaphragme
curseur_diaphragme= tk.Scale(interface, orient='horizontal', from_=1, to=1000,
length=400, 
             label="taille du diaphragme")
curseur_diaphragme.place(x=10,y=50)

# 2e curseur pour la taille du cache
curseur_cache= tk.Scale(interface, orient='horizontal', from_=1, to=10000, 
length=400, 
             label="taille du cache")
curseur_cache.place(x=10,y=120)

# Bouton pour recalculer les transformee de fourier et afficher les nouvelles images
b1 = tk.Button(interface, text ='Lancer', command=lambda:calcul())
b1.place(x=10,y=200)

# Bouton pour arreter la simulation
b3 = tk.Button(interface, text ='Quitter', command=interface.destroy)
b3.pack(side = RIGHT, padx = 10, pady = 10)
b3.place(x=10,y=250)


interface.mainloop()