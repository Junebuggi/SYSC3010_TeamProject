/*
  Created by Emma Boulay on 2019-11-13.
  Copyright © 2019 Emma Boulay. All rights reserved.
*/

#include "stubUltrasonic.h"

stubUltrasonic::stubUltrasonic(){
    currentIndex = 0;
}

float stubUltrasonic::getStubWaterDistance(){
    return waterDistances[currentIndex];
}

void stubUltrasonic::setStubWaterDispensed(){
    if(currentIndex + 1 == sizeof(waterDistances)){
        return;
    }
    currentIndex++;
}

