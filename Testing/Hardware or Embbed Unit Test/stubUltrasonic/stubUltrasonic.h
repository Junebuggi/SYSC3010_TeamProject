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
    float waterDistances[19] = {4.00, 4.25, 4.50, 5.25, 5.50, 5.75,
                                6.00, 6.75, 7.00, 7.25, 7.5, 7.75,
                                8.00, 8.25, 8.50, 8.75, 9.00, 9.25,
                                9.50} ;
    int currentIndex;
};

#endif
