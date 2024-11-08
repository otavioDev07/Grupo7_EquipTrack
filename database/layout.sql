-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema equiptrack
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema equiptrack
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `equiptrack` DEFAULT CHARACTER SET utf8mb3 ;
USE `equiptrack` ;

-- -----------------------------------------------------
-- Table `equiptrack`.`supervisor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `equiptrack`.`supervisor` (
  `idSupervisor` INT NOT NULL AUTO_INCREMENT,
  `nomeSupervisor` VARCHAR(45) NOT NULL,
  `CPF` VARCHAR(11) NOT NULL,
  `senhaAcesso` VARCHAR(60) NOT NULL,
  `status` ENUM('ativo', 'inativo') NOT NULL,
  PRIMARY KEY (`idSupervisor`),
  UNIQUE INDEX `nomeFuncionario_UNIQUE` (`nomeSupervisor` ASC) VISIBLE,
  UNIQUE INDEX `CPF_UNIQUE` (`CPF` ASC) VISIBLE)
ENGINE = InnoDB
<<<<<<< HEAD
AUTO_INCREMENT = 2
=======
AUTO_INCREMENT = 3
>>>>>>> main
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `equiptrack`.`backlog`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `equiptrack`.`backlog` (
  `idBacklog` INT NOT NULL AUTO_INCREMENT,
  `dataHora` TIMESTAMP NOT NULL,
  `acao` VARCHAR(100) NOT NULL,
  `idSupervisor` INT NOT NULL,
  PRIMARY KEY (`idBacklog`),
  INDEX `fk_Backlog_Supervisor1_idx` (`idSupervisor` ASC) VISIBLE,
  CONSTRAINT `fk_Backlog_Supervisor1`
    FOREIGN KEY (`idSupervisor`)
    REFERENCES `equiptrack`.`supervisor` (`idSupervisor`))
ENGINE = InnoDB
<<<<<<< HEAD
AUTO_INCREMENT = 7
=======
AUTO_INCREMENT = 10
>>>>>>> main
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `equiptrack`.`setor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `equiptrack`.`setor` (
  `idSetor` INT NOT NULL AUTO_INCREMENT,
  `nomeSetor` VARCHAR(45) NOT NULL,
  `idSupervisor` INT NOT NULL,
  PRIMARY KEY (`idSetor`),
  INDEX `fk_Setor_Supervisor1_idx` (`idSupervisor` ASC) VISIBLE,
  CONSTRAINT `fk_Setor_Supervisor1`
    FOREIGN KEY (`idSupervisor`)
    REFERENCES `equiptrack`.`supervisor` (`idSupervisor`))
ENGINE = InnoDB
<<<<<<< HEAD
AUTO_INCREMENT = 2
=======
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `equiptrack`.`funcionário`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `equiptrack`.`funcionário` (
  `idFuncionario` INT NOT NULL AUTO_INCREMENT,
  `nomeFuncionário` VARCHAR(45) NOT NULL,
  `NIF` VARCHAR(10) NOT NULL,
  `CPF` CHAR(11) NOT NULL,
  `idSetor` INT NOT NULL,
  `condicoesEspeciais` VARCHAR(300) NULL DEFAULT NULL,
  `cargo` VARCHAR(45) NOT NULL,
  `tamCalcado` CHAR(2) NOT NULL,
  `tamRoupa` VARCHAR(2) NOT NULL,
  `status` ENUM('ativo', 'inativo') NOT NULL DEFAULT 'ativo',
  PRIMARY KEY (`idFuncionario`),
  INDEX `fk_Funcionário_Setor_idx` (`idSetor` ASC) VISIBLE,
  CONSTRAINT `fk_Funcionário_Setor`
    FOREIGN KEY (`idSetor`)
    REFERENCES `equiptrack`.`setor` (`idSetor`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
>>>>>>> main
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `equiptrack`.`epi`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `equiptrack`.`epi` (
  `idEPI` INT NOT NULL AUTO_INCREMENT,
  `codigoCA` INT NOT NULL,
  `numeroSerie` VARCHAR(45) NOT NULL,
  `marca` VARCHAR(45) NOT NULL,
  `modelo` VARCHAR(45) NULL DEFAULT NULL,
  `dataLocacao` DATE NULL DEFAULT NULL,
  `dataVencimento` DATE NOT NULL,
  `status` ENUM('Em uso', 'Estoque') NOT NULL DEFAULT 'Estoque',
  `observacoes` VARCHAR(300) NULL DEFAULT NULL,
  `nomeEquipamento` VARCHAR(45) NOT NULL,
  `dataAquisicao` DATE NOT NULL,
  `tamanho` VARCHAR(45) NULL DEFAULT NULL,
  `quantidade` INT NOT NULL,
  `idSetor` INT NOT NULL,
<<<<<<< HEAD
=======
  `idFuncionario` INT NULL DEFAULT NULL,
>>>>>>> main
  PRIMARY KEY (`idEPI`),
  UNIQUE INDEX `codigoCA_UNIQUE` (`codigoCA` ASC) VISIBLE,
  UNIQUE INDEX `numeroSerie_UNIQUE` (`numeroSerie` ASC) VISIBLE,
  INDEX `fk_EPI_Setor1_idx` (`idSetor` ASC) VISIBLE,
<<<<<<< HEAD
=======
  INDEX `fk_EPI_Funcionario` (`idFuncionario` ASC) VISIBLE,
  CONSTRAINT `fk_EPI_Funcionario`
    FOREIGN KEY (`idFuncionario`)
    REFERENCES `equiptrack`.`funcionário` (`idFuncionario`)
    ON DELETE SET NULL,
>>>>>>> main
  CONSTRAINT `fk_EPI_Setor1`
    FOREIGN KEY (`idSetor`)
    REFERENCES `equiptrack`.`setor` (`idSetor`))
ENGINE = InnoDB
<<<<<<< HEAD
AUTO_INCREMENT = 15
=======
AUTO_INCREMENT = 19
>>>>>>> main
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `equiptrack`.`descarte`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `equiptrack`.`descarte` (
  `idDescarte` INT NOT NULL AUTO_INCREMENT,
  `motivoDescarte` VARCHAR(300) NOT NULL,
  `localDescarte` VARCHAR(150) NOT NULL,
  `dataDescarte` DATE NOT NULL,
  `idEquipamento` INT NOT NULL,
  `quantidade` INT NOT NULL,
  PRIMARY KEY (`idDescarte`),
  INDEX `fk_Descarte_Equipamento1_idx` (`idEquipamento` ASC) VISIBLE,
  CONSTRAINT `fk_Descarte_Equipamento1`
    FOREIGN KEY (`idEquipamento`)
    REFERENCES `equiptrack`.`epi` (`idEPI`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
<<<<<<< HEAD
-- Table `equiptrack`.`funcionário`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `equiptrack`.`funcionário` (
  `idFuncionario` INT NOT NULL AUTO_INCREMENT,
  `nomeFuncionário` VARCHAR(45) NOT NULL,
  `NIF` VARCHAR(10) NOT NULL,
  `CPF` CHAR(11) NOT NULL,
  `idSetor` INT NOT NULL,
  `condições especiais` VARCHAR(300) NOT NULL,
  `cargo` VARCHAR(45) NOT NULL,
  `tamCalcado` CHAR(2) NOT NULL,
  `tamRoupa` VARCHAR(45) NOT NULL,
  `status` ENUM('ativo', 'inativo') NOT NULL,
  PRIMARY KEY (`idFuncionario`),
  INDEX `fk_Funcionário_Setor_idx` (`idSetor` ASC) VISIBLE,
  CONSTRAINT `fk_Funcionário_Setor`
    FOREIGN KEY (`idSetor`)
    REFERENCES `equiptrack`.`setor` (`idSetor`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
=======
>>>>>>> main
-- Table `equiptrack`.`epi_funcionário`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `equiptrack`.`epi_funcionário` (
  `idEPI_Funcionario` INT NOT NULL AUTO_INCREMENT,
  `idEquipamento` INT NOT NULL,
  `idFuncionario` INT NOT NULL,
  `dataHora` TIMESTAMP NOT NULL,
  `quantidade` INT NOT NULL,
  PRIMARY KEY (`idEPI_Funcionario`),
  INDEX `fk_Equipamento_has_Funcionário_Equipamento1_idx` (`idEquipamento` ASC) VISIBLE,
  INDEX `fk_EPI_Funcionário_Funcionário1_idx` (`idFuncionario` ASC) VISIBLE,
  CONSTRAINT `fk_EPI_Funcionário_Funcionário1`
    FOREIGN KEY (`idFuncionario`)
    REFERENCES `equiptrack`.`funcionário` (`idFuncionario`),
  CONSTRAINT `fk_Equipamento_has_Funcionário_Equipamento1`
    FOREIGN KEY (`idEquipamento`)
    REFERENCES `equiptrack`.`epi` (`idEPI`))
ENGINE = InnoDB
<<<<<<< HEAD
AUTO_INCREMENT = 2
=======
AUTO_INCREMENT = 3
>>>>>>> main
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
