from sqlalchemy import Column, Integer, ForeignKey, Date, DateTime, Time, Text, Boolean, Float


from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Section(Base):
    __tablename__ = "Oddiely"
    section_id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("nazov", Text)


class UserInfo(Base):
    __tablename__ = "Kmenovi_clenovia"
    info_id = Column("id", Integer, primary_key=True, autoincrement=True)
    gender = Column("pohlavie", Text)
    birth_date = Column("datum_narodenia", Date)
    birth_country = Column("krajina_narodenia", Text)
    nationality = Column("statna_prislusnost", Text)
    permanent_residence_country = Column("krajina_trvaleho_pobytu", Text)
    street = Column("ulica", Text)
    house_number = Column("cislo_domu", Integer)
    zip_code = Column("pcs", Integer)
    city = Column("mesto", Text)
    phone_number = Column("telefon", Text)
    email = Column("mail", Text)


class User(Base):
    __tablename__ = "Pouzivatelia"
    user_id = Column("id", Integer, primary_key=True, autoincrement=True)
    first_name = Column("meno", Text)
    last_name = Column("priezvisko", Text)
    user_club_id = Column("os_i_c", Text,
                          comment="Unikátne číslo používateľa pridelené klubom, kombinácia čísel a znakov")
    chip_number = Column("cip", Text)
    comment = Column("poznamka", Text)
    section_id = Column("id_oddiel", Integer)
    info_id = Column("id_kmen_clen", Integer)
    success = Column("uspech", Text)


class Competition(Base):
    __tablename__ = "Preteky"
    competition_id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("nazov", Text)
    date = Column("datum", DateTime, comment="Dátum a čas konania preteku")
    signup_deadline = Column("deadline", DateTime)
    is_active = Column("aktiv", Boolean)
    comment = Column("poznamka", Text)

class Competition_categories(Base):
    __tablename__ = "Kategorie_pre"
    comp_cat_id = Column("id", Integer, primary_key=True, autoincrement=True)
    competition_id = Column("id_pret", Integer, ForeignKey("Preteky.id"))
    category_id = Column("id_kat", Integer, ForeignKey("Kategorie.id"))


class Category(Base):
    __tablename__ = "Kategorie"
    category_id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("nazov", Text)


class Signup(Base):
    __tablename__ = "Prihlaseni"
    signup_id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("id_pouz", Integer)
    competition_id = Column("id_pret", Integer)
    category_id = Column("id_kat", Integer)
    comment = Column("poznamka", Text)


class Performance(Base):
    __tablename__ = "Vykon"
    performance_id = Column("id", Integer, primary_key=True, autoincrement=True)
    competition_id = Column("id_pret", Integer, ForeignKey("Preteky.id"))
    user_id = Column("id_log", Integer, ForeignKey("Pouzivatelia.id"))
    time = Column("moj_cas", Integer)
    winner_time = Column("vitaz_cas", Integer)
    location = Column("miesto", Text)
    winner_name = Column("vitaz", Text)
    distance = Column("vzdialenost", Integer)
    ideal_distance = Column("ideal_vzdialenost", Integer)
    speed = Column("rychlost", Integer)
    altitude_change = Column("prevysenie", Integer)
    delta = Column("odchylka", Integer)
    penalty = Column("prirazka", Integer)
    # TODO: is placement the correct description, or does rating fit better?
    placement = Column("hodnotenie", Integer)


class CompetitionAssessment(Base):
    __tablename__ = "Zhodnotenie"
    assessment_id = Column("id", Integer, primary_key=True, autoincrement=True)
    competition_id = Column("id_pret", Integer, ForeignKey("Preteky.id"))
    user_id = Column("id_pouz", Integer, ForeignKey("Pouzivatelia.id"))
    time = Column("cas", Text)


class Export(Base):
    __tablename__ = "Exporty"
    format_string = Column("retazec", Text, primary_key=True)
