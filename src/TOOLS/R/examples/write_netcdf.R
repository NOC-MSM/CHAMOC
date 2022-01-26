







# writing in netcdf output file                                                                                   
# -----------------------------                                                                                   
fileout=paste('figure06_',ensembleid,'_',varid,'.nc',sep='')
XX      = dim.def.ncdf("x",'',seq(x),create_dimvar=TRUE)
YY      = dim.def.ncdf("y",'',seq(y),create_dimvar=TRUE)
#TIME    = dim.def.ncdf("time",timeunit,t.op,create_dimvar=TRUE)                                                  
#TIMEYR  = dim.def.ncdf("timeyr",'year',seq(Nyr),create_dimvar=TRUE)                                              
dem.ye.nc  = var.def.ncdf("dem_ye",unit,list(XX,YY),missval=1.e+30)
dem.jfm.nc = var.def.ncdf("dem_jfm",unit,list(XX,YY),missval=1.e+30)
dem.mam.nc = var.def.ncdf("dem_mam",unit,list(XX,YY),missval=1.e+30)
dem.jja.nc = var.def.ncdf("dem_jja",unit,list(XX,YY),missval=1.e+30)
dem.son.nc = var.def.ncdf("dem_son",unit,list(XX,YY),missval=1.e+30)
pval.ye.nc  = var.def.ncdf("pval_ye","(0-1)",list(XX,YY),missval=1.e+30)
pval.jfm.nc = var.def.ncdf("pval_jfm","(0-1)",list(XX,YY),missval=1.e+30)
pval.mam.nc = var.def.ncdf("pval_mam","(0-1)",list(XX,YY),missval=1.e+30)
pval.jja.nc = var.def.ncdf("pval_jja","(0-1)",list(XX,YY),missval=1.e+30)
pval.son.nc = var.def.ncdf("pval_son","(0-1)",list(XX,YY),missval=1.e+30)
ncnew=create.ncdf(fileout,list(dem.ye.nc,pval.ye.nc,
    dem.jfm.nc,pval.jfm.nc,
    dem.mam.nc,pval.mam.nc,
    dem.jja.nc,pval.jja.nc,
    dem.son.nc,pval.son.nc))
#                                                                                                                 
put.var.ncdf(ncnew,"dem_ye",dem.ye,start=NA,count=dim(dem.ye))
put.var.ncdf(ncnew,"dem_jfm",dem.jfm,start=NA,count=dim(dem.jfm))
put.var.ncdf(ncnew,"dem_mam",dem.mam,start=NA,count=dim(dem.mam))
put.var.ncdf(ncnew,"dem_jja",dem.jja,start=NA,count=dim(dem.jja))
put.var.ncdf(ncnew,"dem_son",dem.son,start=NA,count=dim(dem.son))
put.var.ncdf(ncnew,"pval_ye",pval.ye,start=NA,count=dim(pval.ye))
put.var.ncdf(ncnew,"pval_jfm",pval.jfm,start=NA,count=dim(pval.jfm))
put.var.ncdf(ncnew,"pval_mam",pval.mam,start=NA,count=dim(pval.mam))
put.var.ncdf(ncnew,"pval_jja",pval.jja,start=NA,count=dim(pval.jja))
put.var.ncdf(ncnew,"pval_son",pval.son,start=NA,count=dim(pval.son))
close.ncdf(ncnew)


