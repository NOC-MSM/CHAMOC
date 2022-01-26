# ================================================================
# Qques fonctions de stats utiles #
# ================================================================
# nombre de degré de liberté d'une serie temporelle
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
nf = function(v,na.rm=T){
    
    acf1 = acf(v,plot=F)$acf[2]
    r1 = ifelse(acf1<0,0,acf1)
    N = length(v)
    ndf = round(N*(1-r1)/(1+r1))
    ndf
}

calcndf = function(v1,v2,isatm1=F,isatm2=F){
  acf1 = acf(v1,plot=F)
  acf2 = acf(v2,plot=F)
  acf1pos = ifelse(acf1$acf<0,0,acf1$acf)
  acf2pos = ifelse(acf2$acf<0,0,acf2$acf)
  if (isatm1){
      r1=acf1pos[2]
  } else {
      r1=(acf1pos[2] + sqrt(acf1pos[3]) + (acf1pos[4])^(1/3))/3
  }
  if (isatm2){
      r2=acf2pos[2]
  } else {
      r2=(acf2pos[2] + sqrt(acf2pos[3]) + (acf2pos[4])^(1/3))/3
  }
  N = length(v1)
  ndf = round(N*(1-r1*r2)/(1+r1*r2))
  ndf
}
# Correlation glissante entre 2 series (running correlation)
# ----------------------------------------------------------------
runcor = function(a,b,win=5){
  # si len(a) != len(b) --> erreur
  if (length(a)!=length(b)) {
    print('ERROR in runcor : the two series should have the same length!')
    return()
  }

  # calcule du coef de correlation
  N=length(a)
  coef<-array(dim=N)
  for (i in seq(1,N)){
    if (i<win+1) {
      coef[i]<-cor(a[1:(i+win)],b[1:(i+win)],use="pairwise.complete.obs")
    } else if (i>N-win) {
    coef[i]<-cor(a[(i-win):N],b[(i-win):N],use="pairwise.complete.obs")
    } else {
      coef[i]<-cor(a[(i-win):(i+win)],b[(i-win):(i+win)],use="pairwise.complete.obs")
    }
  }
  coef
} #a.g.
# -------------------------------------------------------------------------
#renvoie une array contenant le nb de valeurs utilisées pour le calcule
# de la correlation à l'indice i (complement de la fonction runcor
# permet d'avoir une idée du nombre de degré de liberté pour le calcule
# de significativité
# ------------------------------------------------------------------------
n_runcor = function(a,b,win=5){
  # si len(a) != len(b) --> erreur
  if (length(a)!=length(b)) {
    print('ERROR in runcor : the two series should have the same length!')
    return()
  }

  # calcule du coef de correlation
  N=length(a)
  n<-array(dim=N)
  for (i in seq(1,N)){
    if (i<win+1) {
      n[i]<-i+win
    } else if (i>N-win) {
      n[i]<-N-(i-win)+1
    } else {
      n[i]<-2*win+1
    }
  }
  n
}
# -------------------------------------------------------------------------
# renvoie une array contenant le nb de degrée de liberté pour le calcule
# de la correlation à l'indice i (complement de la fonction runcor
# utile pour le calcule de significativité
# ------------------------------------------------------------------------
ndf_runcor = function(a,b,win=5){
  # si len(a) != len(b) --> erreur
  if (length(a)!=length(b)) {
    print('ERROR in runcor : the two series should have the same length!')
    return()
  }

  # calcule du coef de correlation
  N=length(a)
  ndf<-array(dim=N)
  for (i in seq(1,N)){
    if (i<win+1) {
      ndf[i]<-i+win
    } else if (i>N-win) {
      ndf[i]<-N-(i-win)+1
    } else {
      ndf[i]<-2*win+1
    }
  }
  ndf
}

# fonction renvoyant le seuil de significativité d'un calcule de corrélation
# Return the limit of significance for the linear correlation coefficient
# at the confidence level conf.
# This limit is calculated according to the Pearson test, considering that the random variable T = r*sqrt(n-2)/sqrt(1-r^2) follows a student distribution with n-2 degrees of freedom.
#
#    INPUTs :
#         n : Int --> 
#         conf : int or float --> Percentage of confidence
#         mod : string --> possible options : 2sided, 1sided
#
#    OUTPUTs :
#         r : float --> threshold value for the correlation coefficient
mycorsignif=function(N,conf,mod='two.sided'){
  ndf  =  N-2
  conf = conf/100
  if (mod=='one.sided') {
    alpha=(1-conf)
  } else if (mod=='two.sided') {
    alpha=(1-conf)/2
  }
  t=qt(alpha,ndf)
  
  r = abs(t/(ndf + t**2)**0.5)
  r
}

# Fonction de correlation entre 2 vecteurs
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fcor = function(a,b,lagmax=10,step=1,lagu='year',conf=95){
  # si len(a) != len(b) --> erreur
  if (length(a)!=length(b)) {
    stop('ERROR in fcor : the two series should have the same length!')
    return()
  }
  if (length(a)<lagmax+3) {
    stop('lagmax larger than length of time series; not enough values for correlation coefficient computation! You should choose lower value for lagmax.')
  }

  # calcule du coef de correlation
  N=length(a)
  lags = seq(from=-lagmax,to=lagmax,by=step)
  coef<-array(dim=2*lagmax+1)
  ssignif <- array(dim=2*lagmax+1)
  i=1
  for (lag in lags){
    if (lag<0) {
     coef[i]<-cor(a[1:(N+lag)],b[(1-lag):N],use="pairwise.complete.obs")
     ndf = length(a[1:(N+lag)])
     ssignif[i] = mycorsignif(ndf,conf=95)
    } else {
    coef[i]<-cor(a[(1+lag):N],b[1:(N-lag)],use="pairwise.complete.obs")
    ndf = length(a[(1+lag):N])
    ssignif[i] = mycorsignif(ndf,conf=95)
    }
    i=i+1
  }

  # pour faire un axe des temps propre des lags: à finir
  to=as.Date("0000-01-01")
  if (lagu=='year') lagday = lagmax*365 + lagmax/4 #4bissex
  if (lagu=='month') lagday = lagmax*30
  if (lagu=='day') lagday = lagmax
  ti = to - lagday
  tf = to + lagday
  lagtime = seq(ti,tf,by=lagu)
  
  list(values=coef,lags=lags,time=lagtime,ssignif=ssignif)
} #a.g.

# EOF ECO (à partir de la fonction matlab de Juliette)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# M est une matrics Nt (temps), Np (espace)
# resultat :
# x : matrice des eofs (champs spaciaux)
# lambda : matrics diagonale des valeurs propres
# t : matrice des séries temporelles
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
eof_eco = function(M){

  if (length(dim(M))>2) {
    error('Wrong dimensions : M should be an NtxNp matrix')
  }
  Nt = dim(M)[1]
  Np = dim(M)[2]
  
  # anomalies (sur les series temporelles) :
  A = scale(M,center=T,scale=F)

  if (Nt>= Np) {
    C=t(A)*A
    

  }
}
