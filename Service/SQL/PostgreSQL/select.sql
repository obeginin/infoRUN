select * from Roles r
select * from Permissions p 
select * from RolePermissions rp
select * from Students s 
select * from PasswordResetTokens pr

select * from Subjects sub 
select * from Variants v
select * from Tasks t 
select * from SubTasks st order by subtaskid desc
select * from SubTasksImages sti order by subtaskid desc
select * from SubTaskFiles stf order by subtaskid desc
select * from SubTaskSolutions sts order by subtaskid desc
SELECT * FROM SubTaskTemp stt order by SubTaskID desc

select * from StudentTasks
select * from StudentActionLogs


SELECT * FROM GetSubtasks();





