from pathlib import Path
import os
import subprocess
import tempfile


def test_make_rd_samplesheet():
    sample_id = "Seq26-100"
    case_id = "first-test-12345"
    referral = "Konstitutionell"
    sex = "F"
    fq_r1 = "Seq26-100_S1_L001_R1_001.fastq,Seq26-100_S1_L002_R1_001.fastq"
    fq_r2 = "Seq26-100_S1_L001_R2_001.fastq,Seq26-100_S1_L002_R2_001.fastq"
    panels = "HTAD_PAN_WGS_v.1.0,OTHER_PAN_WGS_v.1.0"
    with tempfile.TemporaryDirectory() as tmpdirname:
        returncode = subprocess.run(["bash", "actions/make_raredisease_samplesheet.sh", sample_id,
                                     case_id, referral, sex, panels, fq_r1, fq_r2, tmpdirname]
                                    ).returncode
        assert returncode == 0
        with open(tmpdirname + "/samplesheet.csv") as file:
            samplesheet = file.readlines()

    assert len(samplesheet) == 3
    header = ["sample", "lane", "fastq_1", "fastq_2", "sex", "phenotype", "paternal_id",
              "maternal_id", "case_id"]
    samplesheet_header = samplesheet[0].strip().split(",")
    assert samplesheet_header == header

    fq_r1 = fq_r1.split(",")
    fq_r2 = fq_r2.split(",")

    for i in range(1, 3):
        samplesheet_line = samplesheet[i].strip().split(",")
        assert samplesheet_line[0] == sample_id
        assert samplesheet_line[1] == f"L00{str(i)}"
        assert samplesheet_line[2] == fq_r1[i - 1]
        assert samplesheet_line[3] == fq_r2[i - 1]
        assert samplesheet_line[4] == "2"
        assert samplesheet_line[5] == "2"
        assert samplesheet_line[6] == ""
        assert samplesheet_line[7] == ""
        assert samplesheet_line[8] == case_id


def test_wrong_referral_fastq():
    out_dir = Path("workdir")
    out_dir.mkdir(exist_ok=True)
    sample_id = "Seq26-1"
    case_id = "curious-test-12345"
    referral = "InteKonstitutionell"
    sex = "U"
    fq_r1 = "Seq26-1_S1_L001_R1_001.fastq"
    fq_r2 = "Seq26-1_S1_L001_R2_001.fastq"
    panels = "HTAD_PAN_WGS_v.1.0"
    with tempfile.TemporaryDirectory() as tmpdirname:
        returncode = subprocess.run(["bash", "actions/make_raredisease_samplesheet.sh", sample_id,
                                     case_id, referral, sex, panels, fq_r1, fq_r2, tmpdirname]
                                    ).returncode
        assert not os.path.isfile(tmpdirname + "/samplesheet.csv")
    assert returncode == 1


def test_wrong_panel():
    sample_id = "Seq26-1"
    case_id = "another-test-12345"
    referral = "Konstitutionell"
    sex = "U"
    fq_r1 = "Seq26-1_S1_L001_R1_001.fastq"
    fq_r2 = "Seq26-1_S1_L001_R2_001.fastq"
    panels = "OTHER_PAN_WGS_v.1.0"
    with tempfile.TemporaryDirectory() as tmpdirname:
        returncode = subprocess.run(["bash", "actions/make_raredisease_samplesheet.sh", sample_id,
                                    case_id, referral, sex, panels, fq_r1, fq_r2, tmpdirname]
                                    ).returncode
        assert not os.path.isfile(tmpdirname + "/samplesheet.csv")
    assert returncode == 1


def test_unsorted_fastq():
    sample_id = "Seq26-1"
    case_id = "other-test-12345"
    referral = "Konstitutionell"
    sex = "U"
    fq_1 = "Seq26-1_S1_L002_R1_001.fastq,Seq26-1_S1_L003_R1_001.fastq,Seq26-1_S1_L001_R1_001.fastq"
    fq_2 = "Seq26-1_S1_L003_R2_001.fastq,Seq26-1_S1_L002_R2_001.fastq,Seq26-1_S1_L001_R2_001.fastq"
    panels = "HTAD_PAN_WGS_v.1.0,OTHER_PAN_WGS_v.1.0"
    with tempfile.TemporaryDirectory() as tmpdirname:
        returncode = subprocess.run(["bash", "actions/make_raredisease_samplesheet.sh", sample_id,
                                     case_id, referral, sex, panels, fq_1, fq_2, tmpdirname]
                                    ).returncode
        assert os.path.isfile(tmpdirname + "/samplesheet.csv")
        assert returncode == 0

        with open(tmpdirname + "/samplesheet.csv") as file:
            samplesheet = file.readlines()

    assert len(samplesheet) == 4

    fq_1 = fq_1.split(",")
    fq_2 = fq_2.split(",")
    fq_1.sort()
    fq_2.sort()
    for i in range(1, 3):
        samplesheet_line = samplesheet[i].strip().split(",")
        assert samplesheet_line[0] == sample_id
        assert samplesheet_line[1] == f"L00{str(i)}"
        assert samplesheet_line[2] == fq_1[i - 1]
        assert samplesheet_line[3] == fq_2[i - 1]
        assert samplesheet_line[4] == "0"
        assert samplesheet_line[5] == "2"
        assert samplesheet_line[6] == ""
        assert samplesheet_line[7] == ""
        assert samplesheet_line[8] == case_id


def test_uneven_fastq():
    sample_id = "Seq26-1"
    case_id = "last-test-12345"
    referral = "Konstitutionell"
    sex = "U"
    fq_r1 = "Seq26-1_S1_L002_R1_001.fastq,Seq26-1_S1_L003_R1_001.fastq,Seq26-1_S1_L001_R1_001.fastq"
    fq_r2 = "Seq26-1_S1_L003_R2_001.fastq,Seq26-1_S1_L002_R2_001.fastq"
    panels = "HTAD_PAN_WGS_v.1.0,OTHER_PAN_WGS_v.1.0"
    with tempfile.TemporaryDirectory() as tmpdirname:
        returncode = subprocess.run(["bash", "actions/make_raredisease_samplesheet.sh", sample_id,
                                    case_id, referral, sex, panels, fq_r1, fq_r2, tmpdirname]
                                    ).returncode
        assert returncode == 1
        assert not os.path.isfile(tmpdirname + "/samplesheet.csv")

        returncode = subprocess.run(["bash", "actions/make_raredisease_samplesheet.sh", sample_id,
                                    case_id, referral, sex, panels, fq_r2, fq_r1, tmpdirname]
                                    ).returncode
        assert returncode == 1
        assert not os.path.isfile(tmpdirname + "/samplesheet.csv")
