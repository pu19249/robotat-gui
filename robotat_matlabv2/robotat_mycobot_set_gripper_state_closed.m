function robotat_mycobot_set_gripper_state_closed(tcp_obj, robotno)
    if((robotno ~= 1) && (robotno ~= 2))
        error('Selected myCobot does not exist.');
    end
    
    s.dst = robotno+1; % DST_MYCOBOTX
    s.cmd = 5; % CMD_CLOSE_GRIPPER
    s.pld = 0;
    write(tcp_obj, uint8(jsonencode(s)));
end