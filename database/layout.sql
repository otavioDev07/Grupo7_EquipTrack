-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema equipTrack
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema equipTrack
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `equipTrack` DEFAULT CHARACTER SET utf8 ;
USE `equipTrack` ;

-- -----------------------------------------------------
-- Table `equipTrack`.`Supervisor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `equipTrack`.`Supervisor` (
  `idSupervisor` INT NOT NULL AUTO_INCREMENT,
  `nomeSupervisor` VARCHAR(45) NOT NULL,
  `CPF` VARCHAR(11) NOT NULL,
  `senhaAcesso` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`idSupervisor`),
  UNIQUE INDEX `nomeFuncionario_UNIQUE` (`nomeSupervisor` ASC) VISIBLE,
  UNIQUE INDEX `CPF_UNIQUE` (`CPF` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `equipTrack`.`Setor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `equipTrack`.`Setor` (
  `idSetor` INT NOT NULL AUTO_INCREMENT,
  `nomeSetor` VARCHAR(45) NOT NULL,
  `idSupervisor` INT NOT NULL,
  PRIMARY KEY (`idSetor`),
  INDEX `fk_Setor_Supervisor1_idx` (`idSupervisor` ASC) VISIBLE,
  CONSTRAINT `fk_Setor_Supervisor1`
    FOREIGN KEY (`idSupervisor`)
    REFERENCES `equipTrack`.`Supervisor` (`idSupervisor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `equipTrack`.`Categoria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `equipTrack`.`Categoria` (
  `idCategoria` INT NOT NULL AUTO_INCREMENT,
  `nomeCategoria` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idCategoria`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `equipTrack`.`EPI`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `equipTrack`.`EPI` (
  `idEPI` INT NOT NULL AUTO_INCREMENT,
  `codigoCA` INT NOT NULL,
  `numeroSerie` VARCHAR(45) NOT NULL,
  `marca` VARCHAR(45) NOT NULL,
  `modelo` VARCHAR(45) NULL,
  `dataLocacao` DATE NULL,
  `dataVencimento` DATE NOT NULL,
  `status` ENUM("Em uso", "Estoque") NOT NULL,
  `observacoes` VARCHAR(300) NULL,
  `nomeEquipamento` VARCHAR(45) NOT NULL,
  `dataAquisicao` DATE NOT NULL,
  `tamanho` VARCHAR(45) NULL,
  `quantidade` INT NOT NULL,
  `idSetor` INT NOT NULL,
  `idCategoria` INT NOT NULL,
  PRIMARY KEY (`idEPI`),
  INDEX `fk_EPI_Setor1_idx` (`idSetor` ASC) VISIBLE,
  INDEX `fk_EPI_Categoria1_idx` (`idCategoria` ASC) VISIBLE,
  UNIQUE INDEX `codigoCA_UNIQUE` (`codigoCA` ASC) VISIBLE,
  UNIQUE INDEX `numeroSerie_UNIQUE` (`numeroSerie` ASC) VISIBLE,
  CONSTRAINT `fk_EPI_Setor1`
    FOREIGN KEY (`idSetor`)
    REFERENCES `equipTrack`.`Setor` (`idSetor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_EPI_Categoria1`
    FOREIGN KEY (`idCategoria`)
    REFERENCES `equipTrack`.`Categoria` (`idCategoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `equipTrack`.`Funcionário`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `equipTrack`.`Funcionário` (
  `idFuncionario` INT NOT NULL AUTO_INCREMENT,
  `nomeFuncionário` VARCHAR(45) NOT NULL,
  `NIF` VARCHAR(10) NOT NULL,
  `CPF` CHAR(11) NOT NULL,
  `idSetor` INT NOT NULL,
  `condições especiais` VARCHAR(300) NOT NULL,
  `cargo` VARCHAR(45) NOT NULL,
  `tamCalcado` CHAR(2) NOT NULL,
  `tamRoupa` VARCHAR(45) NOT NULL,
  `status` ENUM("ativo", "inativo") NOT NULL,
  PRIMARY KEY (`idFuncionario`),
  INDEX `fk_Funcionário_Setor_idx` (`idSetor` ASC) VISIBLE,
  CONSTRAINT `fk_Funcionário_Setor`
    FOREIGN KEY (`idSetor`)
    REFERENCES `equipTrack`.`Setor` (`idSetor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `equipTrack`.`EPI_Funcionário`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `equipTrack`.`EPI_Funcionário` (
  `idEPI_Funcionario` INT NOT NULL AUTO_INCREMENT,
  `idEquipamento` INT NOT NULL,
  `idFuncionario` INT NOT NULL,
  `dataHora` TIMESTAMP NOT NULL,
  `quantidade` INT NOT NULL,
  INDEX `fk_Equipamento_has_Funcionário_Equipamento1_idx` (`idEquipamento` ASC) VISIBLE,
  PRIMARY KEY (`idEPI_Funcionario`),
  INDEX `fk_EPI_Funcionário_Funcionário1_idx` (`idFuncionario` ASC) VISIBLE,
  CONSTRAINT `fk_Equipamento_has_Funcionário_Equipamento1`
    FOREIGN KEY (`idEquipamento`)
    REFERENCES `equipTrack`.`EPI` (`idEPI`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_EPI_Funcionário_Funcionário1`
    FOREIGN KEY (`idFuncionario`)
    REFERENCES `equipTrack`.`Funcionário` (`idFuncionario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `equipTrack`.`Descarte`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `equipTrack`.`Descarte` (
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
    REFERENCES `equipTrack`.`EPI` (`idEPI`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `equipTrack`.`Backlog`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `equipTrack`.`Backlog` (
  `idBacklog` INT NOT NULL AUTO_INCREMENT,
  `dataHora` TIMESTAMP NOT NULL,
  `acao` VARCHAR(100) NOT NULL,
  `idSupervisor` INT NOT NULL,
  PRIMARY KEY (`idBacklog`),
  INDEX `fk_Backlog_Supervisor1_idx` (`idSupervisor` ASC) VISIBLE,
  CONSTRAINT `fk_Backlog_Supervisor1`
    FOREIGN KEY (`idSupervisor`)
    REFERENCES `equipTrack`.`Supervisor` (`idSupervisor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
