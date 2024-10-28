CREATE TABLE hotel_users
(
  uid  NOT NULL AUTO_INCREMENT,
  password VARCHAR(100) NOT NULL,
  name VARCHAR(100) NOT NULL,
  phone VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  role VARCHAR(30) NOT NULL,
  membership_type INT NOT NULL,
  discount_rate INT NOT NULL,
  free_wifi INT NOT NULL,
  free_water INT NOT NULL,
  points_available INT NOT NULL,
  total_points_gained INT NOT NULL,
  total_points_used INT NOT NULL,
  PRIMARY KEY (uid)
) ENGINE=MyISAM;

CREATE TABLE hotel_reservations
(
  res_id INT NOT NULL,
  check_in_date INT NOT NULL,
  check_out_date INT NOT NULL,
  payment_method INT NOT NULL,
  payment_date INT NOT NULL,
  amount INT NOT NULL,
  points_gained INT NOT NULL,
  uid INT NOT NULL,
  PRIMARY KEY (res_id)
) ENGINE=MyISAM;

CREATE TABLE hotel_rewards_redeemed
(
  transaction_id INT NOT NULL,
  rewards_claimed INT NOT NULL,
  description INT NOT NULL,
  points_used INT NOT NULL,
  uid INT NOT NULL,
  PRIMARY KEY (transaction_id)
) ENGINE=MyISAM;

CREATE TABLE hotel_rooms
(
  room_id INT NOT NULL,
  room_num INT NOT NULL,
  price INT NOT NULL,
  status INT NOT NULL,
  room_type INT NOT NULL,
  description INT NOT NULL,
  res_id INT NOT NULL,
  PRIMARY KEY (room_id)
) ENGINE=MyISAM;
