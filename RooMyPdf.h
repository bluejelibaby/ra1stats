/*****************************************************************************
 * Project: RooFit                                                           *
 *                                                                           *
  * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/

#ifndef ROOMYPDF
#define ROOMYPDF

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"
 
class RooMyPdf : public RooAbsPdf {
public:
  RooMyPdf() {} ; 
  RooMyPdf(const char *name, const char *title,
	      RooAbsReal& _full);
  RooMyPdf(const RooMyPdf& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new RooMyPdf(*this,newname); }
  inline virtual ~RooMyPdf() { }

protected:

  RooRealProxy full ;
 
  
  Double_t evaluate() const ;

private:

  ClassDef(RooMyPdf,1) // Your description goes here...
};
 
#endif
