from pyknow import *
from pyknow import Fact, KnowledgeEngine, Rule, MATCH, OR, AS, NOT

class DetectorCancer(KnowledgeEngine):
    def input_data(self):
        print("=====================================================================================================")
        print("SISTEMA EXPERTO PARA LA DETECCIÓN TEMPRANA DE CÁNCER\n")
        print("\nIngrese sus respuestas en minúscula por favor...\n")
        asim = input("¿El paciente padece asimetría? ")
        edge = input("Ingrese el tipo de borde: ")
        color = input("Ingrese el color: ")
        diam = float(input("Ingrese el diámetro (en milimetros): "))
        evo = input("¿Ha evolucionado? ")

        if asim == "si":
            self.declare(Fact(asimetria=True))
        else:
            self.declare(Fact(asimetria=False))
        if edge == "irregular":
            self.declare(Fact(borde_irregular=True))
        if edge == "regular":
            self.declare(Fact(borde_irregular=False))
        if edge == "desigual":
            self.declare(Fact(borde_desigual=True))
        if edge == "reborde":
            self.declare(Fact(borde_reborde=True))
        if edge == "borroso":
            self.declare(Fact(borde_borroso=True))
        if color == "cafe":
            self.declare(Fact(color_cafe=True))
        if color == "negro":
            self.declare(Fact(color_negro=True))
        if color == "azul" or color == "rojo" or color == "rosado" or color == "blanco":
            self.declare(Fact(color_variado=True))
        if diam <= 3 and diam > 0:
            self.declare(Fact(diam="pequeño"))
        if diam <= 6 and diam > 3:
            self.declare(Fact(diam="mediano"))
        if diam <= 12 and diam > 6:
            self.declare(Fact(diam="grande"))
        if evo == "si":
            self.declare(Fact(evolucion=True))
        else:
            self.declare(Fact(evolucion=False))

    @Rule(Fact(asimetria=True) & Fact(borde_irregular=True) & Fact(color_negro=True))
    def rule_melanoma(self):
        print("El paciente tiene un melanoma. Se requiere evaluación médica inmediata.")

    @Rule(Fact(asimetria=True) & Fact(borde_irregular=False) & Fact(color_cafe=True))
    def rule_nevus(self):
        print("El paciente tiene un nevus. Puede ser benigno, pero se recomienda seguimiento médico.")

    @Rule(Fact(asimetria=True) & Fact(borde_desigual=True) & Fact(diam="grande"))
    def rule_carcinoma(self):
        print("El paciente tiene un carcinoma. Se requiere evaluación médica inmediata.")

    @Rule(Fact(asimetria=False) & Fact(borde_reborde=True) & Fact(color_variado=True) & Fact(evolucion=True))
    def rule_carcinoma_in_situ(self):
        print("El paciente tiene un carcinoma in situ. Puede ser tratable, pero se recomienda seguimiento médico.")

    @Rule(Fact(asimetria=True) & Fact(borde_borroso=True) & Fact(diam="pequeño"))
    def rule_carcinoma_basocelular(self):
        print("El paciente tiene un carcinoma basocelular. Se requiere evaluación médica inmediata.")

    @Rule(OR(Fact(borde_irregular=True), Fact(borde_desigual=True), Fact(borde_reborde=True), Fact(borde_borroso=True)),
          Fact(color_cafe=True), Fact(diam="mediano"))
    def rule_sospecha(self):
        print("El paciente tiene una lesión sospechosa. Se recomienda evaluación médica para descartar patologías graves.")

    @Rule(NOT(Fact(asimetria=True)), NOT(Fact(borde_irregular=True)), NOT(Fact(borde_desigual=True)),
          NOT(Fact(borde_reborde=True)), NOT(Fact(borde_borroso=True)), NOT(Fact(color_cafe=True)),
          NOT(Fact(color_negro=True)), NOT(Fact(color_variado=True)), NOT(Fact(diam="grande")),
          NOT(Fact(evolucion=True)))
    def rule_benigno(self):
        print("La lesión es probablemente benigna. Sin embargo, siempre se recomienda seguimiento médico para confirmación.")

    @Rule(AS._fact << Fact(color_cafe=True) | Fact(color_negro=True) | Fact(color_variado=True),
          AS._fact << Fact(asimetria=True) | Fact(borde_irregular=True) | Fact(borde_desigual=True) |
          Fact(borde_reborde=True) | Fact(borde_borroso=True), NOT(Fact(diam="grande")))
    def rule_lesion_atipica(self):
        print("El paciente tiene una lesión atípica. Se recomienda evaluación médica para determinar el diagnóstico.")

    @Rule(Fact(asimetria=True) & Fact(borde_irregular=True) & Fact(color_cafe=True))
    def rule_carcinoma_in_situ_melanoma(self):
        print("El paciente tiene un carcinoma in situ o melanoma. Se requiere evaluación médica inmediata.")

    @Rule(Fact(asimetria=True) & Fact(borde_irregular=True) & Fact(color_variado=True) & Fact(diam="mediano"))
    def rule_melanoma_probable(self):
        print("El paciente tiene un probable melanoma. Se recomienda evaluación médica para confirmación.")

    @Rule(Fact(borde_irregular=True) & Fact(color_variado=True) & Fact(diam="grande"))
    def rule_carcinoma_probable(self):
        print("El paciente tiene un probable carcinoma. Se recomienda evaluación médica para confirmación.")

    @Rule(Fact(asimetria=True) & Fact(borde_reborde=True) & Fact(color_variado=True) & Fact(diam="mediano"))
    def rule_lesion_melanocitica(self):
        print("El paciente tiene una lesión melanocítica. Se requiere seguimiento médico para descartar patologías graves.")

    @Rule(Fact(asimetria=True) & Fact(borde_irregular=False) & Fact(color_cafe=True) & Fact(diam="pequeño"))
    def rule_nevus_comun(self):
        print("El paciente tiene un nevus común. Es probablemente benigno, pero se recomienda seguimiento médico.")

    @Rule(Fact(asimetria=False) & Fact(borde_irregular=False) & Fact(color_variado=True) & Fact(diam="pequeño"))
    def rule_lesion_benigna(self):
        print("El paciente tiene una lesión probablemente benigna. Se recomienda seguimiento médico para confirmación.")

    @Rule(Fact(borde_borroso=True) & Fact(color_cafe=True) & Fact(diam="grande") & Fact(evolucion=True))
    def rule_carcinoma_probable_basocelular(self):
        print("El paciente tiene un probable carcinoma basocelular. Se requiere evaluación médica inmediata.")

    @Rule(AS._fact << Fact(color_cafe=True) | Fact(color_negro=True) | Fact(color_variado=True),
          AS._ << Fact(borde_irregular=True) | Fact(borde_desigual=True) | Fact(borde_reborde=True) |
          Fact(borde_borroso=True), NOT(Fact(diam="pequeño")))
    def rule_lesion_poco_clara(self):
        print("La lesión es poco clara. Se requiere evaluación médica para un diagnóstico adecuado.")

    @Rule(Fact(asimetria=True) & Fact(borde_irregular=True) & Fact(color_negro=True) & Fact(diam="grande"))
    def rule_melanoma_avanzado(self):
        print("El paciente tiene un melanoma avanzado. Se requiere evaluación médica inmediata y tratamiento urgente.")

    @Rule(Fact(asimetria=True) & Fact(borde_irregular=True) & Fact(color_rojo=True) & Fact(diam="grande"))
    def rule_melanoma_inflamatorio(self):
        print("El paciente tiene un melanoma inflamatorio. Se requiere evaluación médica inmediata y tratamiento urgente.")

    @Rule(Fact(borde_reborde=True) & Fact(color_variado=True) & Fact(diam="grande"))
    def rule_carcinoma_avanzado(self):
        print("El paciente tiene un carcinoma avanzado. Se requiere evaluación médica inmediata y tratamiento urgente.")

    @Rule(Fact(borde_irregular=True) & Fact(color_cafe=True) & Fact(diam="mediano"))
    def rule_nevus_atipico(self):
        print("El paciente tiene un nevus atípico. Se recomienda evaluación médica para determinar el diagnóstico.")
    
    @Rule(Fact(asimetria=True) & Fact(borde_irregular=False) & Fact(color_cafe=True) & Fact(diam="grande") & Fact(evolucion=True))
    def rule_nevus_con_cambios(self):
        print("El paciente tiene un nevus con cambios. Se requiere evaluación médica para determinar su naturaleza.")

    @Rule(Fact(asimetria=False) & Fact(borde_irregular=False) & Fact(color_variado=True) & Fact(diam="grande") & Fact(evolucion=True))
    def rule_lesion_con_cambios(self):
        print("La lesión tiene cambios en su aspecto. Se recomienda evaluación médica para confirmar el diagnóstico.")

    @Rule(AS._fact1 << Fact(asimetria=True), AS._fact2 << Fact(borde_irregular=True), AS._fact3 << Fact(color_variado=True),
          AS._fact4 << Fact(diam="grande"), AS._fact5 << Fact(evolucion=True))
    def rule_lesion_con_caracteristicas_sospechosas(self):
        print("La lesión presenta características sospechosas. Se recomienda evaluación médica para un diagnóstico adecuado.")

    @Rule(Fact(color_negro=True) & Fact(borde_irregular=True) & Fact(diam="grande"))
    def rule_melanoma_avanzado(self):
        print("El paciente tiene un melanoma avanzado. Se requiere evaluación médica inmediata y tratamiento urgente.")

    @Rule(Fact(color_rojo=True) & Fact(asimetria=True) & Fact(diam="grande"))
    def rule_melanoma_inflamatorio(self):
        print("El paciente tiene un melanoma inflamatorio. Se requiere evaluación médica inmediata y tratamiento urgente.")

    @Rule(Fact(borde_reborde=True) & Fact(color_variado=True) & Fact(diam="grande"))
    def rule_carcinoma_avanzado(self):
        print("El paciente tiene un carcinoma avanzado. Se requiere evaluación médica inmediata y tratamiento urgente.")

    @Rule(Fact(borde_irregular=True) & Fact(color_cafe=True) & Fact(diam="mediano"))
    def rule_nevus_atipico(self):
        print("El paciente tiene un nevus atípico. Se recomienda evaluación médica para determinar el diagnóstico.")


if __name__ == "__main__":
    engine = DetectorCancer()
    engine.reset()
    engine.input_data()
    print("\nResultados(s) o recomendaciones: ")
    engine.run()
    print("=====================================================================================================\n")
