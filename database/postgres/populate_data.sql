-- Insert sample data into "users" table
INSERT INTO public.users (user_id, username, password, full_name, email, department_id) VALUES
  (1, 'john_doe', 'password123', 'John Doe', 'john.doe@email.com', 1),
  (2, 'jane_smith', 'pass456', 'Jane Smith', 'jane.smith@email.com', 2),
  -- Add more rows as needed...

-- Insert sample data into "departments" table
INSERT INTO public.departments (department_id, department_name) VALUES
  (1, 'IT'),
  (2, 'HR'),
  -- Add more rows as needed...

-- Insert sample data into "user_attendance" table
INSERT INTO public.user_attendance (attendance_id, user_id, attendance_date) VALUES
  (1, 1, '2024-01-28'),
  (2, 2, '2024-01-29'),
  -- Add more rows as needed...

-- Insert sample data into "admins" table
INSERT INTO public.admins (admin_id, username, password, full_name, email, department_id) VALUES
  (1, 'admin1', 'admin_pass', 'Admin One', 'admin1@email.com', 1),
  (2, 'admin2', 'admin_pass', 'Admin Two', 'admin2@email.com', 2),
  -- Add more rows as needed...

-- Insert sample data into "admin_attendance" table
INSERT INTO public.admin_attendance (attendance_id, admin_id, attendance_date) VALUES
  (1, 1, '2024-01-28'),
  (2, 2, '2024-01-29'),
  -- Add more rows as needed...
