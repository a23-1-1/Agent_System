-- =============================================================
-- DB Demo Studio — MySQL 初始化
-- 表结构对齐 packages/demo-schema/examples/join-query.json
-- =============================================================

CREATE DATABASE IF NOT EXISTS db_demo;
USE db_demo;

-- students 表
CREATE TABLE students (
    id          INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(50) NOT NULL,
    major       VARCHAR(50),
    enrolled_at DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- courses 表（含外键关联 students）
CREATE TABLE courses (
    id           INT PRIMARY KEY AUTO_INCREMENT,
    student_id   INT NOT NULL,
    course_name  VARCHAR(100) NOT NULL,
    score        DECIMAL(5,2),
    semester     VARCHAR(20),
    FOREIGN KEY (student_id) REFERENCES students(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 索引
CREATE INDEX idx_courses_student_id ON courses(student_id);

-- 示例数据（对应 join-query.json 的 2 行结果）
INSERT INTO students (id, name, major, enrolled_at) VALUES
    (1, '张三', '计算机科学', '2024-09-01'),
    (2, '李四', '软件工程', '2024-09-01'),
    (3, '王五', '数据科学', '2024-09-01');

INSERT INTO courses (id, student_id, course_name, score, semester) VALUES
    (1, 1, '数据库原理', 88.5, '2024-秋'),
    (2, 1, '操作系统', 92.0, '2024-秋'),
    (3, 2, '数据库原理', 76.0, '2024-秋'),
    (4, 3, '计算机网络', 85.0, '2024-秋');
