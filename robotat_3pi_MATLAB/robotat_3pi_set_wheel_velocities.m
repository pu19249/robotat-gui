function robotat_3pi_set_wheel_velocities(robot, dphiL, dphiR)
    wheel_maxvel_rpm = 850;
    wheel_minvel_rpm = -850;
    
    if(dphiL > wheel_maxvel_rpm)
        warning(['Left wheel speed saturated to ', num2str(wheel_maxvel_rpm), ' rpm']);
        dphiL = wheel_maxvel_rpm;
    end

    if(dphiR > wheel_maxvel_rpm)
        warning(['Right wheel speed saturated to ', num2str(wheel_maxvel_rpm), ' rpm']);
        dphiR = wheel_maxvel_rpm;
    end

    if(dphiL < wheel_minvel_rpm)
        warning(['Left wheel speed saturated to ', num2str(wheel_minvel_rpm), ' rpm']);
        dphiL = wheel_minvel_rpm;
    end

    if(dphiR < wheel_minvel_rpm)
        warning(['Right wheel speed saturated to ', num2str(wheel_minvel_rpm), ' rpm']);
        dphiR = wheel_minvel_rpm;
    end

    % encode to a simple CBOR array
    cbormsg = uint8(zeros(1, 11));
    cbormsg(1) = 130; % 82 = array(2)
    cbormsg(2) = 250; % FA = single-precision float
    cbormsg(3:6) = fliplr(typecast(single(dphiL), 'uint8'));
    cbormsg(7) = 250; % FA = single-precision float
    cbormsg(8:11) = fliplr(typecast(single(dphiR), 'uint8'));
    
    write(robot.tcpsock, cbormsg);
end