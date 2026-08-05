INSERT INTO logins (ip, user_agent, username, password, country, is_bot) VALUES
-- 5 Bots (Using agents from the list, is_bot = true)
('192.168.1.10', 'curl', 'scanner1', 'password123', 'Russia', TRUE),
('192.168.1.11', 'sqlmap', 'scanner2', 'password123', 'China', TRUE),
('192.168.1.12', 'nmap', 'scanner3', 'password123', 'Brazil', TRUE),
('192.168.1.13', 'python-requests', 'scanner4', 'password123', 'Iran', TRUE),
('192.168.1.14', 'BurpSuite', 'scanner5', 'password123', 'USA', TRUE),

-- 5 Normal Users (Common password AND common username)
('10.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'admin', 'password123', 'USA', FALSE),
('10.0.0.2', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)', 'admin', 'password123', 'UK', FALSE),
('10.0.0.3', 'Mozilla/5.0 (X11; Linux x86_64)', 'admin', 'password123', 'France', FALSE),
('10.0.0.4', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)', 'admin', 'password123', 'Germany', FALSE),
('10.0.0.5', 'Mozilla/5.0 (iPad; CPU OS 14_0)', 'admin', 'password123', 'Canada', FALSE),

-- 5 Normal Users (Common username ONLY)
('172.16.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'admin', 'securePass1', 'USA', FALSE),
('172.16.0.2', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)', 'admin', 'securePass2', 'UK', FALSE),
('172.16.0.3', 'Mozilla/5.0 (X11; Linux x86_64)', 'admin', 'securePass3', 'France', FALSE),
('172.16.0.4', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)', 'admin', 'securePass4', 'Germany', FALSE),
('172.16.0.5', 'Mozilla/5.0 (iPad; CPU OS 14_0)', 'admin', 'securePass5', 'Canada', FALSE),

-- 5 Normal Users (Unique usernames and unique passwords)
('8.8.8.8', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'johndoe', 'qwert123', 'USA', FALSE),
('8.8.4.4', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)', 'janedoe', 'asdf456', 'UK', FALSE),
('1.1.1.1', 'Mozilla/5.0 (X11; Linux x86_64)', 'alice', 'zxcv789', 'France', FALSE),
('9.9.9.9', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)', 'bob', 'letmein99', 'Germany', FALSE),
('208.67.222.222', 'Mozilla/5.0 (iPad; CPU OS 14_0)', 'charlie', 'p@ssword0', 'Canada', FALSE);