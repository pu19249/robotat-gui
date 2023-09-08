function tcp_obj = robotat_connect(ip)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
    port = 1883;
    try
        tcp_obj = tcpclient(ip, port);
    catch
        disp('ERROR: Could not connect to Robotat server.');
    end
end