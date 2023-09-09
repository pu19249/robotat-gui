function robotat_3pi_force_stop(robot)
    dphiL = 0;
    dphiR = 0;

    % encode to a simple CBOR array
    cbormsg = uint8(zeros(1, 11));
    cbormsg(1) = 130; % 82 = array(2)
    cbormsg(2) = 250; % FA = single-precision float
    cbormsg(3:6) = fliplr(typecast(single(dphiL), 'uint8'));
    cbormsg(7) = 250; % FA = single-precision float
    cbormsg(8:11) = fliplr(typecast(single(dphiR), 'uint8'));
    
    write(robot.tcpsock, cbormsg);
end