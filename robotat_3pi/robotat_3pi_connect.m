function robot = robotat_3pi_connect(agent_id)
    if(numel(agent_id) ~= 1)
        error('Can only pair with a single 3Pi agent.');
    end

    agent_id = round(agent_id);
    if(agent_id < 0) || (agent_id > 19)
        error('Invalid agent ID. Allowed IDs: 0 - 19.');
    end
    robot.id = agent_id;

    if(agent_id) > 9
        ip = '192.168.50.1';
    else
        ip = '192.168.50.10';
    end

    ip = [ip, num2str(agent_id)];
    robot.ip = ip;
    robot.port = 8888;

    try
        tcpsock = tcpclient(robot.ip, robot.port);
        robot.tcpsock = tcpsock;
    catch
        disp('ERROR: Could not connect to the robot.');
    end
end