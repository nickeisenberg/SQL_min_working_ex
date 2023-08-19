import faker
import numpy as np

faker.Faker.seed(0)

fk = faker.Faker()

JOBS = [fk.job() for i in range(15)]
JOB_ID = {j: i + 1 for i, j in enumerate(JOBS)}
SALARY_AVG = np.array([
    35, 95, 65, 210, 45, 95, 165, 120, 44, 76, 55, 67, 43, 84, 29
])
SALARY_AVG = {j: s for j, s in zip(JOBS, SALARY_AVG)}
SALARY_AVG['unemployed'] = 0

