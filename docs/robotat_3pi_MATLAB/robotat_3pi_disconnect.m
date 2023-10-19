function robotat_3pi_disconnect(robot)
    evalin('base', ['clear ', inputname(1)]);
    disp('Disconnected from robot.');
end