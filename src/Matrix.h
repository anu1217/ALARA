/* $Id: Matrix.h,v 1.6 2002-08-05 20:23:19 fateneja Exp $ */
#include "alara.h"

#ifndef MATRIX_H
#define MATRIX_H

#include "Chains/Chain.h"

// NEED COMMENT This class has no comments

class Matrix
{
  friend void Chain::fillTMat(Matrix&, double, int);
  friend void Chain::setDecay(Matrix&, double);
  friend void Chain::mult(Matrix&, Matrix&, Matrix&);

protected:
  int size;
  double *data;

  void square();

public:
  Matrix() { size = 0; data = NULL; };
  Matrix(int);
  Matrix(const Matrix&);
  Matrix(double*,int,int);
  ~Matrix();

  Matrix operator*(const Matrix&);
  Matrix& operator*=(const Matrix&);
  Matrix operator^(int);
  Matrix& operator=(const Matrix&);
  double& operator[](int idx) { return data[idx]; };

  int getSize() { return size; };

  double rowSum(int);

};

#endif
