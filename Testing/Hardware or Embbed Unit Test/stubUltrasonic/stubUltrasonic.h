/*
  Created by Emma Boulay on 2019-11-13.
  Copyright © 2019 Emma Boulay. All rights reserved.
*/

#ifndef stubUltrasonic_h
#define stubUltrasonic_h

class stubUltrasonic
{
  public:
    stubUltrasonic();
    float getStubWaterDistance();
    void setStubWaterDispensed();
  private:
    float waterDistances[7] = {4.00, 5.00, 6.00, 7.00, 8.00, 9.00,                              10.00} ;
    int currentIndex;
    int n;
};

#endif
