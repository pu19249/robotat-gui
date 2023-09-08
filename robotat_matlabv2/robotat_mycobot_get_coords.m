function xi = robotat_mycobot_get_coords(tcp_obj, robotno)
    if((robotno ~= 1) && (robotno ~= 2))
        error('Selected myCobot does not exist.');
    end

    timeout_count = 0;
    timeout_in100ms = 2 / 0.1; % time to wait for data to arrive
    
    s.dst = robotno+1; % DST_MYCOBOTX
    s.cmd = 1; % CMD_GET_POSE
    s.pld = 0;
    write(tcp_obj, uint8(jsonencode(s)));

    while((tcp_obj.BytesAvailable == 0) && (timeout_count < timeout_in100ms))
        timeout_count = timeout_count + 1;
        pause(0.1);
    end

    if(timeout_count == timeout_in100ms)
        error('Could not receive data from server.');
    else
        xi = jsondecode(char(read(tcp_obj)));
    end
end