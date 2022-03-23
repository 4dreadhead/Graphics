from numba import njit


class MathHelper:
    @staticmethod
    @njit(fastmath=True)
    def determinant(matrix_0: tuple, matrix_1: tuple, matrix_2: tuple) -> int:
        result = matrix_0[0] * matrix_1[1] * matrix_2[2] \
                 - matrix_0[0] * matrix_1[2] * matrix_2[1] \
                 - matrix_0[1] * matrix_1[0] * matrix_2[2] \
                 + matrix_0[1] * matrix_1[2] * matrix_2[0] \
                 + matrix_0[2] * matrix_1[0] * matrix_2[1] \
                 - matrix_0[2] * matrix_1[1] * matrix_2[0]
        return result

    @staticmethod
    @njit(fastmath=True)
    def z_calculate(x, y, determinant_a, determinant_b, determinant_c, determinant_d):
        return (determinant_b * y - determinant_a * x + determinant_d) / \
               determinant_c if determinant_c != 0 else (determinant_b * y - determinant_a * x + determinant_d)

    @staticmethod
    def z_frequency(apex_a, apex_b, apex_c, x, y):
        determinant_a = MathHelper.determinant((apex_a[1], apex_a[2], 1),
                                               (apex_b[1], apex_b[2], 1),
                                               (apex_c[1], apex_c[2], 1))

        determinant_b = MathHelper.determinant((apex_a[0], apex_a[2], 1),
                                               (apex_b[0], apex_b[2], 1),
                                               (apex_c[0], apex_c[2], 1))

        determinant_c = MathHelper.determinant((apex_a[0], apex_a[1], 1),
                                               (apex_b[0], apex_b[1], 1),
                                               (apex_c[0], apex_c[1], 1))

        determinant_d = MathHelper.determinant((apex_a[0], apex_a[1], apex_a[2]),
                                               (apex_b[0], apex_b[1], apex_b[2]),
                                               (apex_c[0], apex_c[1], apex_c[2]))

        z_calculated = MathHelper.z_calculate(x, y, determinant_a, determinant_b, determinant_c, determinant_d)
        return z_calculated

    # Sort apexes of triangle by 'y' coordinates
    @staticmethod
    def sort_apexes(triangle, ascending=False, descending=False):
        for _ in range(3):
            for index in range(1, 3):
                if descending:
                    if triangle[index][1] < triangle[index - 1][1]:
                        triangle[index], triangle[index - 1] = triangle[index - 1], triangle[index]
        return triangle

    # Calculation of color for polygons (to get a three-dimensional image) by depth 'z'
    @staticmethod
    def set_color_step(polygon, z_max, z_color_step):
        return round((z_max - polygon[0][2]) / z_color_step) - int((z_max/z_color_step) / 10)


