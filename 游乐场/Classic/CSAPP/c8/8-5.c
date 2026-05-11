unsigned int snooze(unsigned int secs){
    unsigned int res = sleep(secs);

    printf("Slept for %d of %d secs.\n", 
        secs-res, secs);
    return res;
}