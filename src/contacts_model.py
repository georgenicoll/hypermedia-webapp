import json
import time
from contextlib import suppress
from threading import Thread
from random import random


# ========================================================
# Contact Model
# ========================================================
PAGE_SIZE = 100
MODEL_FILE = "dev-data/db.json"

class Contact:

    # mock contacts database - we store this in a file
    db = {}

    @classmethod
    def load_db(cls):
        print("Loading contacts...")
        with suppress(FileNotFoundError):
            with open('contacts.json', 'r') as contacts_file:
                contacts = json.load(contacts_file)
                cls.db.clear()
                for c in contacts:
                    cls.db[c['id']] = cls(c['id'], c['first'], c['last'], c['phone'], c['email'])
                print(f"Loaded {len(contacts)} contact(s)")

    @classmethod
    def save_db(cls):
        print(f"Saving {len(cls.db)} contacts...")
        out_arr = [c.__dict__ for c in cls.db.values()]
        with open("contacts.json", "w") as f:
            json.dump(out_arr, f, indent=2)

    def __init__(self, id_=None, first=None, last=None, phone=None, email=None):
        self.id = id_
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email
        self.errors = {}

    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    def update(self, first, last, phone, email):
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email
        Contact.save_db()

    def validate(self):
        if not self.email:
            self.errors['email'] = "Email Required"
        existing_contact = next(filter(lambda c: c.id != self.id and c.email == self.email, Contact.db.values()), None)
        if existing_contact:
            self.errors['email'] = "Email Must Be Unique"
        return len(self.errors) == 0

    def save(self):
        if not self.validate():
            return False
        if self.id is None:
            if len(Contact.db) == 0:
                max_id = 1
            else:
                max_id = max(contact.id for contact in Contact.db.values())
            self.id = max_id + 1
            Contact.db[self.id] = self
        Contact.save_db()
        return True

    def delete(self):
        del Contact.db[self.id]
        Contact.save_db()

    @classmethod
    def count(cls):
        time.sleep(2)
        return len(cls.db)

    @classmethod
    def all(cls, page=1):
        page = int(page)
        start = (page - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        return list(cls.db.values())[start:end]

    @classmethod
    def search(cls, text):
        result = []
        for c in cls.db.values():
            match_first = c.first is not None and text in c.first
            match_last = c.last is not None and text in c.last
            match_email = c.email is not None and text in c.email
            match_phone = c.phone is not None and text in c.phone
            if match_first or match_last or match_email or match_phone:
                result.append(c)
        return result

    @classmethod
    def find(cls, id_):
        id_ = int(id_)
        c = cls.db.get(id_)
        if c is not None:
            c.errors = {}

        return c

Contact.load_db()


class Archiver:
    archive_status = "Waiting"
    archive_progress = 0
    thread = None

    def status(self):
        return Archiver.archive_status

    def progress(self):
        return Archiver.archive_progress

    def run(self):
        if Archiver.archive_status == "Waiting":
            Archiver.archive_status = "Running"
            Archiver.archive_progress = 0
            Archiver.thread = Thread(target=self.run_impl)
            Archiver.thread.start()

    def run_impl(self):
        for i in range(10):
            time.sleep(1 * random())
            if Archiver.archive_status != "Running":
                return
            Archiver.archive_progress = (i + 1) / 10
            print("Here... " + str(Archiver.archive_progress))
        time.sleep(1)
        if Archiver.archive_status != "Running":
            return
        Archiver.archive_status = "Complete"

    def archive_file(self):
        return 'contacts.json'

    def reset(self):
        Archiver.archive_status = "Waiting"

    @classmethod
    def get(cls):
        return Archiver()

