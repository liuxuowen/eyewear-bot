-- Database schema for eyewear bot
-- This is a reference schema. Adjust according to your actual database structure.

-- Create leads table
CREATE TABLE IF NOT EXISTS `leads` (
  `leads_id` VARCHAR(50) PRIMARY KEY,
  `leads_date` DATE NOT NULL,
  `sales` VARCHAR(100) NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_leads_date` (`leads_date`),
  INDEX `idx_sales` (`sales`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create sales_orders table
CREATE TABLE IF NOT EXISTS `sales_orders` (
  `order_id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_date` DATE NOT NULL,
  `sales` VARCHAR(100) NOT NULL,
  `leads_id` VARCHAR(50) NOT NULL,
  `sales_price` DECIMAL(10, 2) NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_order_date` (`order_date`),
  INDEX `idx_leads_id` (`leads_id`),
  INDEX `idx_sales` (`sales`),
  FOREIGN KEY (`leads_id`) REFERENCES `leads`(`leads_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Sample data for testing (optional)
-- INSERT INTO `leads` (`leads_id`, `leads_date`, `sales`) VALUES
-- ('LEAD001', '2024-01-15', '张三'),
-- ('LEAD002', '2024-01-15', '李四'),
-- ('LEAD003', '2024-01-15', '王五');

-- INSERT INTO `sales_orders` (`order_date`, `sales`, `leads_id`, `sales_price`) VALUES
-- ('2024-01-15', '张三', 'LEAD001', 1500.00),
-- ('2024-01-15', '李四', 'LEAD002', 2300.00);
