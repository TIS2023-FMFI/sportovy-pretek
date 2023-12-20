from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from . import models


class SectionSchema(SQLAlchemySchema):
    class Meta:
        model = models.Section
        load_instance = True

    id = auto_field("section_id")
    nazov = auto_field("name")


class UserInfoSchema(SQLAlchemySchema):
    class Meta:
        model = models.UserInfo
        load_instance = True

    id = auto_field("info_id")
    pohlavie = auto_field("gender")
    datum_narodenia = auto_field("birth_date")
    krajina_narodenia = auto_field("birth_country")
    statna_prislusnost = auto_field("nationality")
    krajina_trvaleho_pobytu = auto_field("permanent_residence_country")
    ulica = auto_field("street")
    cislo_domu = auto_field("house_number")
    psc = auto_field("zip_code")
    mesto = auto_field("city")
    telefon = auto_field("phone_number")
    mail = auto_field("email")


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = models.User
        load_instance = True

    id = auto_field("user_id")
    meno = auto_field("first_name")
    priezvisko = auto_field("last_name")
    os_i_c = auto_field("user_club_id")
    cip = auto_field("chip_number")
    poznamka = auto_field("comment")
    id_oddiel = auto_field("section_id")
    id_kmen_clen = auto_field("info_id")
    uspech = auto_field("success")


class CompetitionSchema(SQLAlchemySchema):
    class Meta:
        model = models.Competition
        load_instance = True

    id = auto_field("competition_id")
    nazov = auto_field("name")
    datum = auto_field("date")
    deadline = auto_field("signup_deadline")
    aktiv = auto_field("is_active")
    poznamka = auto_field("comment")


class CategorySchema(SQLAlchemySchema):
    class Meta:
        model = models.Category
        load_instance = True

    id = auto_field("comp_cat_id")
    id_pret = auto_field("competition_id")
    id_kat = auto_field("category_id")


class SignupSchema(SQLAlchemySchema):
    class Meta:
        model = models.Signup
        load_instance = True

    id = auto_field("signup_id")
    id_pouz = auto_field("user_id")
    id_pret = auto_field("competition_id")
    id_kat = auto_field("category_id")
    poznamka = auto_field("comment")


class PerformanceSchema(SQLAlchemySchema):
    class Meta:
        model = models.Performance
        load_instance = True

    id = auto_field("performance_id")
    id_pret = auto_field("competition_id")
    id_log = auto_field("user_id")
    moj_cas = auto_field("time")
    vitaz_cas = auto_field("winner_time")
    miesto = auto_field("location")
    vitaz = auto_field("winner_name")
    vzdialenost = auto_field("distance")
    ideal_vzdialenost = auto_field("ideal_distance")
    rychlost = auto_field("speed")
    prevysenie = auto_field("altitude_change")
    odchylka = auto_field("delta")
    prirazka = auto_field("penalty")
    hodnotenie = auto_field("placement")


class CompetitionAssessmentSchema(SQLAlchemySchema):
    class Meta:
        model = models.CompetitionAssessment
        load_instance = True

    id = auto_field("assessment_id")
    id_pret = auto_field("competition_id")
    id_pouz = auto_field("user_id")
    cas = auto_field("time")


class ExportSchema(SQLAlchemySchema):
    class Meta:
        model = models.Export
        load_instance = True

    retazec = auto_field("format_string")
