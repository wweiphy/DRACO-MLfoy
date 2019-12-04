import os
import sys
import numpy as np
import json
import pickle
import math
from array import array
import ROOT
import tqdm
import matplotlib.pyplot as plt

# local imports
filedir  = os.path.dirname(os.path.realpath(__file__))
DRACOdir = os.path.dirname(filedir)
basedir  = os.path.dirname(DRACOdir)
sys.path.append(basedir)

# import with ROOT
from pyrootsOfTheCaribbean.evaluationScripts import plottingScripts

# imports with keras
import utils.generateJTcut as JTcut
import data_frame
import Derivatives
from Derivatives import Inputs, Outputs, Derivatives

import tensorflow.keras
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.models as models
import tensorflow.keras.layers as layer
from tensorflow.keras import backend as K
import pandas as pd

# Limit gpu usage
import tensorflow as tf
import tensorflow_probability as tfp
tfd = tfp.distributions

import matplotlib.pyplot as plt

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
K.set_session(tf.Session(config=config))

class EarlyStopping(tf.keras.callbacks.Callback):
    ''' custom implementation of early stopping
        with options for
            - stopping when val/train loss difference exceeds a percentage threshold
            - stopping when val loss hasnt increased for a set number of epochs '''

    def __init__(self, monitor = "loss", value = None, min_epochs = 20, stopping_epochs = None, patience = 10, verbose = 0):
        super(tf.keras.callbacks.Callback, self).__init__()
        self.val_monitor = "val_"+monitor
        self.train_monitor = monitor
        self.patience = patience
        self.n_failed = 0

        self.stopping_epochs = stopping_epochs
        self.best_epoch = 0
        self.best_validation = 999.
        self.min_epochs = min_epochs
        self.value = value
        self.verbose = verbose

    def on_epoch_end(self, epoch, logs = {}):
        current_val = logs.get(self.val_monitor)
        if epoch == 0:
            self.best_validation = current_val
        current_train = logs.get(self.train_monitor)

        if current_val is None or current_train is None:
            warnings.warn("Early stopping requires {} and {} available".format(
                self.val_monitor, self.train_monitor), RuntimeWarning)

        if current_val < self.best_validation:
            self.best_validation = current_val
            self.best_epoch = epoch

        # check loss by percentage difference
        if self.value:
            if (current_val-current_train)/(current_train) > self.value and epoch > self.min_epochs:
                if self.verbose > 0:
                    print("\nEpoch {}: early stopping threshold reached".format(epoch))
                self.n_failed += 1
                if self.n_failed > self.patience:
                    self.model.stop_training = True

        # check loss by validation performance increase
        if self.stopping_epochs:
            if self.best_epoch + self.stopping_epochs < epoch and epoch > self.min_epochs:
                if self.verbose > 0:
                    print("\nValidation loss has not decreased for {} epochs".format( epoch - self.best_epoch ))
                self.model.stop_training = True


class BNN():
    def __init__(self,
            save_path,
            input_samples,
            category_name,
            train_variables,
            category_cutString = None,
            category_label     = None,
            norm_variables     = True,
            train_epochs       = 500,
            test_percentage    = 0.2,
            eval_metrics       = None,
            shuffle_seed       = None,
            balanceSamples     = False,
            evenSel            = None):

        # save some information
        # list of samples to load into dataframe
        self.input_samples = input_samples

        # output directory for results
        self.save_path = save_path
        if not os.path.exists(self.save_path):
            os.makedirs( self.save_path )

        # name of event category (usually nJet/nTag category)
        self.category_name = category_name

        # string containing event selection requirements;
        # if not specified (default), deduced via JTcut
        self.category_cutString = (category_cutString if category_cutString is not None else JTcut.getJTstring(category_name))
        # category label (string);
        # if not specified (default), deduced via JTcut
        self.category_label = (category_label if category_label is not None else JTcut.getJTlabel (category_name))

        # selection
        self.evenSel = ""
        self.oddSel = "1."
        if not evenSel == None:
            if evenSel == True:
                self.evenSel = "(Evt_Odd==0)"
                self.oddSel  = "(Evt_Odd==1)"
            elif evenSel == False:
                self.evenSel = "(Evt_Odd==1)"
                self.oddSel  = "(Evt_Odd==0)"

        # list of input variables
        self.train_variables = train_variables

        # percentage of events saved for testing
        self.test_percentage = test_percentage

        # number of train epochs
        self.train_epochs = train_epochs

        # additional metrics for evaluation of the training process
        self.eval_metrics = eval_metrics

        # normalize variables in DataFrame
        self.norm_variables = norm_variables

        # load data set
        self.data = self._load_datasets(shuffle_seed, balanceSamples)
        self.event_classes = self.data.output_classes

        # save variable norm
        self.cp_path = self.save_path+"/checkpoints/"
        if not os.path.exists(self.cp_path):
            os.makedirs(self.cp_path)

        if self.norm_variables:
           out_file = self.cp_path + "/variable_norm.csv"
           self.data.norm_csv.to_csv(out_file)
           print("saved variabe norms at "+str(out_file))

        # make plotdir
        self.plot_path = self.save_path+"/plots/"
        if not os.path.exists(self.plot_path):
            os.makedirs(self.plot_path)

        # layer names for in and output (needed for c++ implementation)
        self.inputName = "inputLayer"
        self.outputName = "outputLayer"

    def _load_datasets(self, shuffle_seed, balanceSamples):
        ''' load data set '''
        return data_frame.DataFrame(
            input_samples    = self.input_samples,
            event_category   = self.category_cutString,
            train_variables  = self.train_variables,
            test_percentage  = self.test_percentage,
            norm_variables   = self.norm_variables,
            shuffleSeed      = shuffle_seed,
            balanceSamples   = balanceSamples,
            evenSel          = self.evenSel,
        )

    def _load_architecture(self, config):
        ''' load the architecture configs '''

        # define default network configuration
        self.architecture = {
          "layers":                   [20],
          "loss_function":            "neg_log_likelihood",
          "batch_size":               2000,
          "optimizer":                optimizers.Adam(1e-3),
          "activation_function":      "relu",
          "output_activation":        "Sigmoid",
          "earlystopping_percentage": None,
          "earlystopping_epochs":     None,
        }

        for key in config:
            self.architecture[key] = config[key]

    def load_trained_model(self, inputDirectory):
        ''' load an already trained model '''
        checkpoint_path = inputDirectory+"/checkpoints/trained_model.h5py"

        # get the keras model
        self.model = keras.models.load_model(checkpoint_path)
        self.model.summary()

        # evaluate test dataset with keras model
        self.model_eval = self.model.evaluate(self.data.get_test_data(as_matrix = True), self.data.get_test_labels())

        # save predicitons
        test_pred  = []
        #train_pred = []
        print "Calculating the mean and std: "
        for i in tqdm.tqdm(range(5)):
            test_pred_vector = self.model.predict(self.data.get_test_data (as_matrix = True))
            #train_pred_vector  = self.model.predict(self.data.get_train_data (as_matrix = True))
            test_pred.append(test_pred_vector)
            #train_pred.append(train_pred_vector)

        test_preds = np.concatenate(test_pred, axis=1)
        #train_preds = np.concatenate(train_pred, axis=1)
        self.model_prediction_vector = np.mean(test_preds, axis=1)
        #self.model_train_prediction  = np.mean(train_preds, axis=1)
        self.model_prediction_vector_std = np.std(test_preds, axis=1)
        #self.model_train_prediction_std  = np.std(train_preds, axis=1)

        # print evaluations  with keras model
        from sklearn.metrics import roc_auc_score
        self.roc_auc_score = roc_auc_score(self.data.get_test_labels(), self.model_prediction_vector)
        print("\nROC-AUC score: {}".format(self.roc_auc_score))

        return self.model_prediction_vector, self.model_prediction_vector_std

    def build_default_model(self):
        ''' build default straight forward BNN from architecture dictionary '''

        # infer number of input neurons from number of train variables
        number_of_input_neurons     = self.data.n_input_neurons

        # get all the architecture settings needed to build model
        number_of_neurons_per_layer = self.architecture["layers"]
        activation_function         = self.architecture["activation_function"]
        output_activation           = self.architecture["output_activation"]

        # Specify the posterior distributions for kernel and bias
        def posterior(kernel_size, bias_size=0, dtype=None):
            n = kernel_size + bias_size
            c = np.log(np.expm1(1.))
            return tf.keras.Sequential([
                tfp.layers.VariableLayer(2 * n, dtype=dtype),
                tfp.layers.DistributionLambda(lambda t: tfd.Independent(tfd.Normal(loc=t[..., :n], scale=1e-5 + tf.nn.softplus(c + t[..., n:])), reinterpreted_batch_ndims=1)),
                ])

        # Specify the prior distributions for kernel and bias
        def prior(kernel_size, bias_size=0, dtype=None):
            n = kernel_size + bias_size
            c = np.log(np.expm1(1.))
            return tf.keras.Sequential([
                tfp.layers.VariableLayer(2*n, dtype=dtype),
                tfp.layers.DistributionLambda(lambda t: tfd.Independent(tfd.Normal(loc=t[:n], scale=1e-5 + tf.nn.softplus(c + t[n:])), reinterpreted_batch_ndims=1)),
                ])

        # define input layer
        Inputs = layer.Input(
            shape = (number_of_input_neurons,),
            name  = self.inputName)
        X = Inputs
        self.layer_list = [X]

        ## loop over dense layers
        for iLayer, nNeurons in enumerate(number_of_neurons_per_layer):
            X = tfp.layers.DenseVariational(
                units               = nNeurons,
                make_posterior_fn   = posterior,
                make_prior_fn       = prior,
                kl_weight           = self.architecture["batch_size"] / self.data.get_train_data(as_matrix = True).shape[0],
                activation          = activation_function,
                name                = "DenseLayer_"+str(iLayer)
                )(X)

        # generate output layer
        X = tfp.layers.DenseVariational(
            units               = self.data.n_output_neurons,
            make_posterior_fn   = posterior,
            make_prior_fn       = prior,
            kl_weight           = self.architecture["batch_size"] / self.data.get_train_data(as_matrix = True).shape[0],
            activation          = output_activation.lower(),
            name                = self.outputName
            )(X)

        # define model
        model = models.Model(inputs = [Inputs], outputs = [X])
        model.summary()

        return model

    def build_model(self, config = None, model = None):
        ''' build a BNN model
            use options defined in 'config' dictionary '''

        if config:
            self._load_architecture(config)
            print("loading non default net configs")

        if model == None:
            print("building model from config")
            model = self.build_default_model()

        # custom loss definition
        def neg_log_likelihood(y_true, y_pred):
            sigma = 1.
            dist = tfp.distributions.Normal(loc=y_pred, scale=sigma)
            return -dist.log_prob(y_true)   # tf.math.reduce_mean(input_tensor=dist.log_prob(y_true))

        # compile the model
        model.compile(
            loss        = neg_log_likelihood,
            optimizer   = self.architecture["optimizer"],
            metrics     = self.eval_metrics)

        # save the model
        self.model = model

        # save net information
        out_file    = self.save_path+"/model_summary.yml"
        yml_model   = self.model.to_yaml()
        with open(out_file, "w") as f:
            f.write(yml_model)

    def train_model(self):
        ''' train the model '''

        # add early stopping if activated
        callbacks = None
        if self.architecture["earlystopping_percentage"] or self.architecture["earlystopping_epochs"]:
            callbacks = [EarlyStopping(
                monitor         = "loss",
                value           = self.architecture["earlystopping_percentage"],
                min_epochs      = 50,
                stopping_epochs = self.architecture["earlystopping_epochs"],
                verbose         = 1)]

        # train main net
        self.trained_model = self.model.fit(
            x = self.data.get_train_data(as_matrix = True),
            y = self.data.get_train_labels(),
            batch_size          = self.architecture["batch_size"],
            epochs              = self.train_epochs,
            shuffle             = True,
            callbacks           = callbacks,
            validation_split    = 0.25,
            sample_weight       = self.data.get_train_weights(),
            )

    def eval_model(self):

        # evaluate test dataset
        self.model_eval = self.model.evaluate(
            self.data.get_test_data(as_matrix = True),
            self.data.get_test_labels())

        # save history of eval metrics
        self.model_history = self.trained_model.history

        # save predicitons
        test_pred  = []
        #train_pred = []
        print "Calculating the mean and std: "
        for i in tqdm.tqdm(range(50)):
            test_pred_vector = self.model.predict(self.data.get_test_data (as_matrix = True))
            #train_pred_vector  = self.model.predict(self.data.get_train_data (as_matrix = True))
            test_pred.append(test_pred_vector)
            #train_pred.append(train_pred_vector)

        test_preds = np.concatenate(test_pred, axis=1)
        #train_preds = np.concatenate(train_pred, axis=1)
        self.model_prediction_vector = np.mean(test_preds, axis=1)
        #self.model_train_prediction  = np.mean(train_preds, axis=1)
        self.model_prediction_vector_std = np.std(test_preds, axis=1)
        #self.model_train_prediction_std  = np.std(train_preds, axis=1)

        # print evaluations
        from sklearn.metrics import roc_auc_score
        self.roc_auc_score = roc_auc_score(self.data.get_test_labels(), self.model_prediction_vector)
        print("\nROC-AUC score: {}".format(self.roc_auc_score))

        if self.eval_metrics:
            print("model test loss: {}".format(self.model_eval[0]))
            for im, metric in enumerate(self.eval_metrics):
                print("model test {}: {}".format(metric, self.model_eval[im+1]))
        #return self.model_prediction_vector, self.model_prediction_vector_std

    def save_model(self, argv, execute_dir, netConfigName):
        ''' save the trained model '''

        # save executed command
        argv[0] = execute_dir+"/"+argv[0].split("/")[-1]
        execute_string = "python "+" ".join(argv)
        out_file = self.cp_path+"/command.sh"
        with open(out_file, "w") as f:
            f.write(execute_string)
        print("saved executed command to {}".format(out_file))

        # save model as h5py file
        out_file = self.cp_path + "/trained_model.h5py"
        self.model.save(out_file)
        print("saved trained model at "+str(out_file))

        # save config of model
        model_config = self.model.get_config()
        out_file = self.cp_path +"/trained_model_config"
        with open(out_file, "w") as f:
            f.write( str(model_config))
        print("saved model config at "+str(out_file))

        # save weights of network
        out_file = self.cp_path +"/trained_model_weights.h5"
        self.model.save_weights(out_file)
        print("wrote trained weights to "+str(out_file))

        # set model as non trainable
        for layer in self.model.layers:
            layer.trainable = False
        self.model.trainable = False

        self.netConfig = netConfigName

        # save checkpoint files (needed for c++ implementation)
        out_file = self.cp_path + "/trained_model"
        saver = tf.train.Saver()
        sess = K.get_session()
        save_path = saver.save(sess, out_file)
        print("saved checkpoint files to "+str(out_file))

        # produce json file with configs
        configs = self.architecture
        configs["inputName"] = self.inputName
        configs["outputName"] = self.outputName+"/"+configs["output_activation"]
        configs = {key: configs[key] for key in configs if not "optimizer" in key}

        # more information saving
        configs["inputData"] = self.input_samples.input_path
        configs["eventClasses"] = self.input_samples.getClassConfig()
        configs["JetTagCategory"] = self.category_name
        configs["categoryLabel"] = self.category_label
        configs["Selection"] = self.category_cutString
        configs["trainEpochs"] = self.train_epochs
        configs["trainVariables"] = self.train_variables
        configs["shuffleSeed"] = self.data.shuffleSeed
        configs["trainSelection"] = self.evenSel
        configs["evalSelection"] = self.oddSel
        configs["netConfig"] = self.netConfig

        # save information for binary DNN
        if self.data.binary_classification:
            configs["binaryConfig"] = {
              "minValue": self.input_samples.bkg_target,
              "maxValue": 1.,
            }

        json_file = self.cp_path + "/net_config.json"
        with open(json_file, "w") as jf:
            json.dump(configs, jf, indent = 2, separators = (",", ": "))
        print("wrote net configs to "+str(json_file))

        '''  save configurations of variables for plotscript '''
        plot_file = self.cp_path+"/plot_config.csv"
        variable_configs = pd.read_csv(basedir+"/pyrootsOfTheCaribbean/plot_configs/variableConfig.csv").set_index("variablename", drop = True)
        variables = variable_configs.loc[self.train_variables]
        variables.to_csv(plot_file, sep = ",")
        print("wrote config of input variables to {}".format(plot_file))

        # Serialize the test inputs for the analysis of the gradients
        pickle.dump(self.data.get_test_data(), open(self.cp_path+"/inputvariables.pickle", "wb"))

    # --------------------------------------------------------------------
    # result plotting functions
    # --------------------------------------------------------------------
    def plot_binaryOutput(self, log = False, privateWork = False, printROC = False,
                        nbins = None, bin_range = [0.,1.], name = "binary_discriminator",
                        sigScale = -1):

        if not nbins:
            nbins = int(50*(1.-bin_range[0]))

        binaryOutput = plottingScripts.plotBinaryOutput(
            data                = self.data,
            test_predictions    = self.model_prediction_vector,
            train_predictions   = None,#self.model_train_prediction,
            nbins               = nbins,
            bin_range           = bin_range,
            event_category      = self.category_label,
            plotdir             = self.save_path,
            logscale            = log,
            sigScale            = sigScale)

        bkg_hist, sig_hist = binaryOutput.plot(ratio = False, printROC = printROC, privateWork = privateWork, name = name)

        from matplotlib.colors import LogNorm
        plt.hist2d(self.model_prediction_vector, self.model_prediction_vector_std, bins=[40,40], cmin=1, norm=LogNorm())
        plt.colorbar()
        plt.xlabel("$\mu$", fontsize = 16)
        plt.ylabel("$\sigma$", fontsize = 16)
        plt.savefig(self.save_path+"/sigma_over_mu.png")
        print "sigma_over_mu.png was created"
        plt.savefig(self.save_path+"/sigma_over_mu.pdf")
        print "sigma_over_mu.pdf was created"
        plt.close()

        # sig_values_std = [ self.model_prediction_vector_std[k] for k in range(len(self.model_prediction_vector_std)) if self.data.get_test_labels()[k] == 1 ]
        # bkg_values_std = [ self.model_prediction_vector_std[k] for k in range(len(self.model_prediction_vector_std)) if not self.data.get_test_labels()[k] == 1 ]
        # sf = len(bkg_values_std) / len(sig_values_std)
        # plt.hist(bkg_values_std, 30, range=[0.0, 0.1], facecolor='orange', edgecolor='black', label='background', alpha=0.5)
        # plt.hist(sig_values_std, 30, range=[0.0, 0.1], histtype='step', edgecolor='blue', label='signal')
        # plt.xlim(0.0, 0.1)
        # plt.xlabel("$\sigma$", fontsize = 16)
        # plt.ylabel("$Events$", fontsize = 16)
        # plt.legend(loc='upper right')
        # plt.savefig(self.save_path+"/sigma.pdf")
        # print "sigma.pdf was created"
        # plt.close()

        binaryOutput_std = plottingScripts.plotBinaryOutput(
            data                = self.data,
            test_predictions    = self.model_prediction_vector_std,
            train_predictions   = None,#self.model_train_prediction_std,
            nbins               = 30,
            bin_range           = [0.,0.1],
            event_category      = self.category_label,
            plotdir             = self.save_path,
            logscale            = log,
            sigScale            = sigScale,
            save_name           = "sigma_discriminator"
            )

        bkg_std_hist, sig_std_hist = binaryOutput_std.plot(ratio = False, printROC = printROC, privateWork = privateWork, name = "\sigma of the Discriminator")

    def plot_metrics(self, privateWork = False):
        plt.rc('text', usetex=True)

        ''' plot history of loss function and evaluation metrics '''
        metrics = ["loss"]
        if self.eval_metrics: metrics += self.eval_metrics

        # loop over metrics and generate matplotlib plot
        for metric in metrics:
            plt.clf()
            # get history of train and validation scores
            train_history = self.model_history[metric]
            val_history = self.model_history["val_"+metric]

            n_epochs = len(train_history)
            epochs = np.arange(1,n_epochs+1,1)

            # plot histories
            plt.plot(epochs, train_history, "b-", label = "train", lw = 2)
            plt.plot(epochs, val_history, "r-", label = "validation", lw = 2)
            if privateWork:
                plt.title("CMS private work", loc = "left", fontsize = 16)

            # add title
            title = self.category_label
            title = title.replace("\\geq", "$\geq$")
            title = title.replace("\\leq", "$\leq$")
            plt.title(title, loc = "right", fontsize = 16)

            # make it nicer
            plt.grid()
            plt.xlabel("epoch", fontsize = 16)
            plt.ylabel(metric.replace("_"," "), fontsize = 16)
            #plt.ylim(ymin=0.)

            # add legend
            plt.legend()

            # save
            out_path = self.save_path + "/model_history_"+str(metric)+".pdf"
            plt.savefig(out_path)
            print("saved plot of "+str(metric)+" at "+str(out_path))
            plt.close()
