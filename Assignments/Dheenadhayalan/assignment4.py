{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "collapsed_sections": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "source": [
        "#1.Download the dataset\n",
        "# 2.Import required library"
      ],
      "metadata": {
        "id": "_UnOLW0-AC9v"
      }
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "2nTxL_4R_uSj"
      },
      "outputs": [],
      "source": [
        "import pandas as pd\n",
        "import numpy as np\n",
        "from sklearn.model_selection import train_test_split\n",
        "from sklearn.preprocessing import LabelEncoder\n",
        "from keras.models import Model\n",
        "from keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding\n",
        "from keras.optimizers import RMSprop\n",
        "from keras.preprocessing.text import Tokenizer\n",
        "from keras_preprocessing import sequence\n",
        "from keras.utils import to_categorical\n",
        "from keras.models import load_model"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "#3.Read Dataset and do preprocessing"
      ],
      "metadata": {
        "id": "IouuXumUAWiA"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "df = pd.read_csv('/content/drive/MyDrive/spam.csv',delimiter=',',encoding='latin-1')\n",
        "df.head()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 206
        },
        "id": "MMrZdULKAdPj",
        "outputId": "b2473186-f6ac-4f20-a7e7-ad0b6e668330"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "     v1                                                 v2 Unnamed: 2  \\\n",
              "0   ham  Go until jurong point, crazy.. Available only ...        NaN   \n",
              "1   ham                      Ok lar... Joking wif u oni...        NaN   \n",
              "2  spam  Free entry in 2 a wkly comp to win FA Cup fina...        NaN   \n",
              "3   ham  U dun say so early hor... U c already then say...        NaN   \n",
              "4   ham  Nah I don't think he goes to usf, he lives aro...        NaN   \n",
              "\n",
              "  Unnamed: 3 Unnamed: 4  \n",
              "0        NaN        NaN  \n",
              "1        NaN        NaN  \n",
              "2        NaN        NaN  \n",
              "3        NaN        NaN  \n",
              "4        NaN        NaN  "
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-f57c0290-0e62-4251-aa54-6a8953c2ca7a\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>v1</th>\n",
              "      <th>v2</th>\n",
              "      <th>Unnamed: 2</th>\n",
              "      <th>Unnamed: 3</th>\n",
              "      <th>Unnamed: 4</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>ham</td>\n",
              "      <td>Go until jurong point, crazy.. Available only ...</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>ham</td>\n",
              "      <td>Ok lar... Joking wif u oni...</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>spam</td>\n",
              "      <td>Free entry in 2 a wkly comp to win FA Cup fina...</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>ham</td>\n",
              "      <td>U dun say so early hor... U c already then say...</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>ham</td>\n",
              "      <td>Nah I don't think he goes to usf, he lives aro...</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-f57c0290-0e62-4251-aa54-6a8953c2ca7a')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "        \n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "      \n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-f57c0290-0e62-4251-aa54-6a8953c2ca7a button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-f57c0290-0e62-4251-aa54-6a8953c2ca7a');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n",
              "  "
            ]
          },
          "metadata": {},
          "execution_count": 2
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'],axis=1,inplace=True) #dropping unwanted columns\n",
        "df.info()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "3dynkSZsBfr4",
        "outputId": "13e2ee35-0116-4274-b939-940505d92d6e"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "<class 'pandas.core.frame.DataFrame'>\n",
            "RangeIndex: 5572 entries, 0 to 5571\n",
            "Data columns (total 2 columns):\n",
            " #   Column  Non-Null Count  Dtype \n",
            "---  ------  --------------  ----- \n",
            " 0   v1      5572 non-null   object\n",
            " 1   v2      5572 non-null   object\n",
            "dtypes: object(2)\n",
            "memory usage: 87.2+ KB\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Count of Spam and Ham values\n",
        "df.groupby(['v1']).size()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "m26wRkcTBhl_",
        "outputId": "43a0eb27-e55d-40fb-a5cd-b35b67a2ecdc"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "v1\n",
              "ham     4825\n",
              "spam     747\n",
              "dtype: int64"
            ]
          },
          "metadata": {},
          "execution_count": 4
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Label Encoding target column\n",
        "X = df.v2\n",
        "Y = df.v1\n",
        "le = LabelEncoder()\n",
        "Y = le.fit_transform(Y)\n",
        "Y = Y.reshape(-1,1)"
      ],
      "metadata": {
        "id": "vz9FFb7VB3Mn"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Test and train split\n",
        "X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.15)"
      ],
      "metadata": {
        "id": "2JgncJ0XCJd-"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Tokenisation function\n",
        "max_words = 1000\n",
        "max_len = 150\n",
        "tok = Tokenizer(num_words=max_words)\n",
        "tok.fit_on_texts(X_train)\n",
        "sequences = tok.texts_to_sequences(X_train)\n",
        "\n",
        "sequences_matrix = sequence.pad_sequences(sequences,maxlen=max_len)"
      ],
      "metadata": {
        "id": "gzKo8tS3CQtF"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "# 4.Create Model and 5. Add Layers (LSTM, Dense-(Hidden Layers), Output)"
      ],
      "metadata": {
        "id": "lloH3xf1CdEQ"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Creating LSTM model\n",
        "inputs = Input(name='InputLayer',shape=[max_len])\n",
        "layer = Embedding(max_words,50,input_length=max_len)(inputs)\n",
        "layer = LSTM(64)(layer)\n",
        "layer = Dense(256,name='FullyConnectedLayer1')(layer)\n",
        "layer = Activation('relu')(layer)\n",
        "layer = Dropout(0.5)(layer)\n",
        "layer = Dense(1,name='OutputLayer')(layer)\n",
        "layer = Activation('sigmoid')(layer)"
      ],
      "metadata": {
        "id": "LcdWT_pbCfHU"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "# 6.Compile the model"
      ],
      "metadata": {
        "id": "3QQtqI9XCrq8"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "model = Model(inputs=inputs,outputs=layer)\n",
        "model.summary()\n",
        "model.compile(loss='binary_crossentropy',optimizer=RMSprop(),metrics=['accuracy'])"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "6taAGNkbCtK8",
        "outputId": "58d7ed97-82b6-42de-edec-56e4a80f3348"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Model: \"model\"\n",
            "_________________________________________________________________\n",
            " Layer (type)                Output Shape              Param #   \n",
            "=================================================================\n",
            " InputLayer (InputLayer)     [(None, 150)]             0         \n",
            "                                                                 \n",
            " embedding (Embedding)       (None, 150, 50)           50000     \n",
            "                                                                 \n",
            " lstm (LSTM)                 (None, 64)                29440     \n",
            "                                                                 \n",
            " FullyConnectedLayer1 (Dense  (None, 256)              16640     \n",
            " )                                                               \n",
            "                                                                 \n",
            " activation (Activation)     (None, 256)               0         \n",
            "                                                                 \n",
            " dropout (Dropout)           (None, 256)               0         \n",
            "                                                                 \n",
            " OutputLayer (Dense)         (None, 1)                 257       \n",
            "                                                                 \n",
            " activation_1 (Activation)   (None, 1)                 0         \n",
            "                                                                 \n",
            "=================================================================\n",
            "Total params: 96,337\n",
            "Trainable params: 96,337\n",
            "Non-trainable params: 0\n",
            "_________________________________________________________________\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# 7.Fit the Model"
      ],
      "metadata": {
        "id": "yt06PXzwC4Nr"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "model.fit(sequences_matrix,Y_train,batch_size=128,epochs=10,\n",
        "          validation_split=0.2)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "4rE9j5kbC5rT",
        "outputId": "12c392ff-3a5f-4dd0-9eb9-8dceec3b0c5d"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Epoch 1/10\n",
            "30/30 [==============================] - 12s 284ms/step - loss: 0.3184 - accuracy: 0.8728 - val_loss: 0.1240 - val_accuracy: 0.9705\n",
            "Epoch 2/10\n",
            "30/30 [==============================] - 8s 263ms/step - loss: 0.0872 - accuracy: 0.9794 - val_loss: 0.0685 - val_accuracy: 0.9821\n",
            "Epoch 3/10\n",
            "30/30 [==============================] - 8s 262ms/step - loss: 0.0442 - accuracy: 0.9868 - val_loss: 0.0492 - val_accuracy: 0.9863\n",
            "Epoch 4/10\n",
            "30/30 [==============================] - 8s 263ms/step - loss: 0.0333 - accuracy: 0.9892 - val_loss: 0.0460 - val_accuracy: 0.9863\n",
            "Epoch 5/10\n",
            "30/30 [==============================] - 8s 264ms/step - loss: 0.0272 - accuracy: 0.9918 - val_loss: 0.0435 - val_accuracy: 0.9884\n",
            "Epoch 6/10\n",
            "30/30 [==============================] - 8s 264ms/step - loss: 0.0210 - accuracy: 0.9934 - val_loss: 0.0933 - val_accuracy: 0.9789\n",
            "Epoch 7/10\n",
            "30/30 [==============================] - 8s 267ms/step - loss: 0.0166 - accuracy: 0.9952 - val_loss: 0.0461 - val_accuracy: 0.9905\n",
            "Epoch 8/10\n",
            "30/30 [==============================] - 8s 266ms/step - loss: 0.0149 - accuracy: 0.9955 - val_loss: 0.0429 - val_accuracy: 0.9884\n",
            "Epoch 9/10\n",
            "30/30 [==============================] - 9s 311ms/step - loss: 0.0113 - accuracy: 0.9976 - val_loss: 0.0497 - val_accuracy: 0.9905\n",
            "Epoch 10/10\n",
            "30/30 [==============================] - 8s 264ms/step - loss: 0.0087 - accuracy: 0.9979 - val_loss: 0.0592 - val_accuracy: 0.9873\n"
          ]
        },
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "<keras.callbacks.History at 0x7f2ec29c78d0>"
            ]
          },
          "metadata": {},
          "execution_count": 10
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# 8.Save the Model"
      ],
      "metadata": {
        "id": "GhImpM3ZDVES"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "model.save(\"model.h1\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "HpsCin9KDWdN",
        "outputId": "380d4b99-1c7c-4b10-8ebf-3dbd7a718f69"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "WARNING:absl:Function `_wrapped_model` contains input name(s) InputLayer with unsupported characters which will be renamed to inputlayer in the SavedModel.\n",
            "WARNING:absl:Found untraced functions such as lstm_cell_layer_call_fn, lstm_cell_layer_call_and_return_conditional_losses while saving (showing 2 of 2). These functions will not be directly callable after loading.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# 9.Test the model"
      ],
      "metadata": {
        "id": "miQ45qh4Dd3J"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "test_sequences = tok.texts_to_sequences(X_test)\n",
        "test_sequences_matrix  = sequence.pad_sequences(test_sequences,maxlen=max_len)"
      ],
      "metadata": {
        "id": "a48BDJcQDfmx"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "accuracy = model.evaluate(test_sequences_matrix,Y_test)\n",
        "print('Accuracy: {:0.3f}'.format(accuracy[1]))"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "gVtZhR-TER-H",
        "outputId": "ff444c92-959e-40dd-87f1-961fd7204a10"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "27/27 [==============================] - 1s 25ms/step - loss: 0.0646 - accuracy: 0.9880\n",
            "Accuracy: 0.988\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "y_pred = model.predict(test_sequences_matrix)\n",
        "print(y_pred[25:40].round(3))"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "EjyTUxXCEVGn",
        "outputId": "f3f5f87f-2cae-4c44-95c5-799943d1179f"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "27/27 [==============================] - 1s 22ms/step\n",
            "[[0.   ]\n",
            " [0.   ]\n",
            " [0.   ]\n",
            " [1.   ]\n",
            " [0.   ]\n",
            " [0.   ]\n",
            " [0.   ]\n",
            " [0.   ]\n",
            " [0.001]\n",
            " [0.   ]\n",
            " [0.   ]\n",
            " [0.   ]\n",
            " [0.001]\n",
            " [0.   ]\n",
            " [0.   ]]\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "print(Y_test[25:40])"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "HUyj8GX8EbFW",
        "outputId": "413bef39-b2be-4cb0-dbc0-510905c1dff7"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "[[0]\n",
            " [0]\n",
            " [0]\n",
            " [1]\n",
            " [0]\n",
            " [0]\n",
            " [0]\n",
            " [0]\n",
            " [0]\n",
            " [0]\n",
            " [0]\n",
            " [0]\n",
            " [0]\n",
            " [0]\n",
            " [0]]\n"
          ]
        }
      ]
    }
  ]
}