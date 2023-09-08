function robotat_mycobot_send_angles(tcp_obj, robotno, q)
    if((robotno ~= 1) && (robotno ~= 2))
        error('Selected myCobot does not exist.');
    end
    
    if(sum(abs(q) > 165) > 0)
        error('Joint angle(s) out of range.');
    end

    s.dst = robotno+1; % DST_MYCOBOTX
    s.cmd = 2; % CMD_SET_CONFIG
    s.pld = q;
    write(tcp_obj, uint8(jsonencode(s)));
end